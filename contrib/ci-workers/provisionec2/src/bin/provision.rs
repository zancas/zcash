#![deny(unsafe_code)]
use rusoto_ec2::{
    DescribeInstancesRequest, DescribeInstancesResult, Ec2, Filter, Reservation, Tag,
    TagSpecification,
};
fn main() {
    let client = rusoto_ec2::Ec2Client::new(rusoto_core::Region::UsEast2);
    let run_instance_request = rusoto_ec2::RunInstancesRequest {
        dry_run: Some(false),
        image_id: Some(String::from("ami-0b3c43897b5d26f4a")),
        min_count: 1,
        max_count: 1,
        key_name: Some(String::from("rsa_aws_ec2")),
        instance_type: Some(String::from("m5.4xlarge")),
        tag_specifications: Some(vec![TagSpecification {
            resource_type: Some(String::from("instance")),
            tags: Some(vec![Tag {
                key: Some(String::from("amibuilder")),
                value: Some(String::from("test1")),
            }]),
        }]),
        ..Default::default()
    };
    client
        .run_instances(run_instance_request)
        .sync()
        .unwrap()
        .instances
        .unwrap();
    let describe_instance_request = DescribeInstancesRequest {
        dry_run: Some(false),
        filters: Some(vec![
            Filter {
                name: Some(String::from("tag:amibuilder")),
                values: Some(vec![String::from("test1")]),
            },
            Filter {
                name: Some(String::from("instance-state-code")),
                values: Some(vec![String::from("16")]),
            },
        ]),
        ..Default::default()
    };
    let reservations = loop {
        let reservations = extract_reservations(
            client
                .describe_instances(describe_instance_request.clone())
                .sync()
                .unwrap(),
        );
        if *reservations != [] {
            break reservations;
        }
        std::thread::sleep(std::time::Duration::new(1, 500_000_000));
    };
    let pub_ip = loop {
        let pub_ip = extract_pub_ip(&extract_reservations(
            client
                .describe_instances(describe_instance_request.clone())
                .sync()
                .unwrap(),
        ));
        if pub_ip != "" {
            break pub_ip;
        }
        std::thread::sleep(std::time::Duration::new(1, 500_000_000));
    };
    use std::io::Write;
    std::fs::File::create("ec2workerpublicIPv4.txt")
        .unwrap()
        .write_all(&pub_ip.replace("\"", "").into_bytes())
        .unwrap();
    let ssh_out = loop {
        let output = std::process::Command::new("ssh")
            .args(&["-o", "StrictHostKeyChecking=no"])
            .args(&["-i", "rsa_aws_ec2"])
            .arg(format!("ubuntu@{}", pub_ip))
            .output()
            .expect("Couldn't run ssh");
        let mut err_output = String::from_utf8(output.stderr).unwrap();
        let error_end = err_output.split_off(92);
        if err_output != "Pseudo-terminal will not be allocated because stdin is not a terminal.\r\nssh: connect to host" {
            break output.stdout;
        }
        std::thread::sleep(std::time::Duration::new(10, 0));
    };
}

fn extract_reservations(describe_instances_result: DescribeInstancesResult) -> Vec<Reservation> {
    describe_instances_result.reservations.unwrap()
}

fn extract_pub_ip(reservations: &Vec<Reservation>) -> String {
    assert_eq!(reservations.len(), 1);
    reservations[0].instances.as_ref().unwrap()[0]
        .public_ip_address
        .as_ref()
        .unwrap()
        .clone()
}

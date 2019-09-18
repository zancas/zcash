#![deny(unsafe_code)]
use rusoto_ec2::{
    DescribeInstancesRequest, DescribeInstancesResult, Ec2, Ec2Client, Filter, Instance,
    Reservation, Tag, TagSpecification,
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
    let reservations = loop {
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
        let reservations = extract_reservations(
            client
                .describe_instances(describe_instance_request)
                .sync()
                .unwrap(),
        );
        if *reservations != [] {
            break reservations;
        }
    };
    println!("{:#?}", reservations);
}

fn extract_reservations(describe_instances_result: DescribeInstancesResult) -> Vec<Reservation> {
    describe_instances_result.reservations.unwrap()
}

fn extract_pub_ip(reservations: &Vec<Reservation>) -> String {
    reservations[0].instances.as_ref().unwrap()[0]
        .public_ip_address
        .as_ref()
        .unwrap()
        .clone()
}

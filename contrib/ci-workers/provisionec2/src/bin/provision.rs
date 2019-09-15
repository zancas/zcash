#![deny(unsafe_code)]
use rusoto_ec2::Ec2;
fn main() {
    let client = rusoto_ec2::Ec2Client::new(rusoto_core::Region::UsEast1);
    let run_instance_request = rusoto_ec2::RunInstancesRequest {
        dry_run: Some(true),
        image_id: Some(String::from("ami-0006ea01070db4b0d")),
        min_count: 1,
        max_count: 1,
        ..Default::default()
    };
    println!(
        "{:#?}",
        client.run_instances(run_instance_request).sync().unwrap()
    );
}

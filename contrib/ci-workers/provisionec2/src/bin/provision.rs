#![deny(unsafe_code)]
use rusoto_ec2::{Ec2, Filter};
fn main() {
    let client = rusoto_ec2::Ec2Client::new(rusoto_core::Region::UsEast1);
    let run_instance_request = rusoto_ec2::RunInstancesRequest {
        dry_run: Some(true),
        image_id: Some(String::from("ami-0006ea01070db4b0d")),
        ..Default::default()
    };
    println!(
        "{:#?}",
        client.run_instances(run_instance_request).sync().unwrap()
    );
}

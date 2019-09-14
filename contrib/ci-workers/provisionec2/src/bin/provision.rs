#![deny(unsafe_code)]
//use structopt::StructOpt;
use rusoto_ec2::Ec2;
fn main() {
    //let cred_provide =
    //    rusoto_credential::StaticProvider::new_minimal("foo".to_string(), "spam".to_string());
    let client = rusoto_ec2::Ec2Client::new(rusoto_core::Region::UsEast1);
    let image_description_request = rusoto_ec2::DescribeImagesRequest {
        dry_run: Some(true),
        executable_users: None,
        filters: None,
        image_ids: None,
        owners: None,
    };
    client.describe_images(image_description_request);
}

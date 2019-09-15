#![deny(unsafe_code)]
//use structopt::StructOpt;
use rusoto_ec2::{Ec2, Filter};
fn main() {
    //let cred_provide =
    //    rusoto_credential::StaticProvider::new_minimal("foo".to_string(), "spam".to_string());
    let client = rusoto_ec2::Ec2Client::new(rusoto_core::Region::UsEast1);
    let image_description_request = rusoto_ec2::DescribeImagesRequest {
        dry_run: Some(false),
        executable_users: Some(vec!["all".to_string()]),
        filters: Some(vec![
            Filter {
                name: Some(String::from("architecture")),
                values: Some(vec![String::from("x86_64")]),
            },
            Filter {
                name: Some(String::from("state")),
                values: Some(vec![String::from("available")]),
            },
        ]),
        image_ids: None,
        owners: Some(vec!["aws-marketplace".to_string()]),
    };
    println!(
        "{:#?}",
        client
            .describe_images(image_description_request)
            .sync()
            .unwrap()
    );
}

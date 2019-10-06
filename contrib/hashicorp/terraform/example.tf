provider "aws" {
  region     = "us-east-2"
}

resource "aws_instance" "example" {
  ami           = "ami-0b69d56e5ac998d57"
  instance_type = "t2.micro"
}


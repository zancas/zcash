provider "aws" {
  profile    = "default"
  region     = "us-east-2"
}

resource "aws_instance" "example" {
  ami           = "ami-0d6b292a6493faf38"
  instance_type = "t2.micro"
}


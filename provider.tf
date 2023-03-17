provider "aws" {
  region = var.aws_region

  skip_get_ec2_platforms  = true
  skip_metadata_api_check = true
}

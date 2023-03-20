variable "aws_region" {

}


variable "environment" {
  description = "AWS Environment"
  type        = string
  default     = "dev"

}


variable "vpc_id" {

}

variable "vpc_subnet_ids" {
  type = list(string)


}

variable "availability_zone" {

}



variable "create_nat_gw" {
  description = "Set to true to deploy NAT Gateway"
  type        = bool

}


variable "s3_bucket_name" {

}

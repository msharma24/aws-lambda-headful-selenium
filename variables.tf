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

module "selenium_lambda_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "4.3.0"

  name        = "${var.environment}-selenium-lambda-sg"
  description = "selenium Lambda Security group"
  vpc_id      = var.vpc_id

  ingress_rules = ["https-443-tcp", "http-80-tcp"]
  ingress_cidr_blocks = [
    "0.0.0.0/0"

  ]

  egress_rules = ["all-all"]

  egress_with_self = [
    {
      rule = "all-all"
    }

  ]
}

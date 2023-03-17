module "selenium_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.environment}-selenium-headful-lambda"
  description   = "Selenium lambda function"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  create_role   = true

  memory_size = "128"
  timeout     = "60"

  source_path            = "./python/lambda_function.py"
  local_existing_package = module.package_dir.local_filename
  create_package         = false
  attach_network_policy  = true


  vpc_subnet_ids         = [aws_subnet.nat_gw_subnet.id]
  vpc_security_group_ids = [module.selenium_lambda_security_group.security_group_id]



  tags = {
    Name = "${var.environment}-selenium-Lambda"
  }


}


module "selenium_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.environment}-selenium-schedule-lambda"
  description   = "Selenium lambda function"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  create_role   = true

  memory_size = "128"
  timeout     = "60"

  source_path           = "./python/lambda_function.py"
  attach_network_policy = true


  vpc_subnet_ids         = var.vpc_subnet_ids
  vpc_security_group_ids = [module.selenium_lambda_security_group.security_group_id]

  environment_variables = {
    TEST_ENV_VAR = "Hello Test Env var"
  }

  tags = {
    Name = "${var.environment}-selenium-Lambda"
  }


}


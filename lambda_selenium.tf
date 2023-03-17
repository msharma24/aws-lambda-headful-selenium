module "selenium_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.environment}-selenium-headful-lambda"
  description   = "Selenium lambda function"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  create_role   = true

  memory_size = "128"
  timeout     = "120"

  source_path            = "./python/lambda_function.py"
  local_existing_package = module.package_dir.local_filename
  create_package         = false
  attach_network_policy  = true


  vpc_subnet_ids         = [aws_subnet.nat_gw_subnet.id]
  vpc_security_group_ids = [module.selenium_lambda_security_group.security_group_id]

  environment_variables = {
    S3_BUCKET     = var.s3_bucket_name
    S3_OBJECT_KEY = "chromedriver"

  }


  tags = {
    Name = "${var.environment}-selenium-Lambda"
  }

  attach_policy_json = true
  policy_json        = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [

              "s3:GetObject",
              "s3:PutObject",
              "s3:GetObjectTagging",
              "s3:ListBucket",
              "s3:GetObjectVersion",
              "ec2:CreateNetworkInterface",
              "ec2:DeleteNetworkInterface",
              "ec2:DescribeNetworkInterfaces",
              "ec2:DetachNetworkInterface"

            ],
            "Resource": ["*"]
        },
        {
          "Effect": "Allow",
          "Action": [
            "sqs:GetQueueUrl",
            "sqs:SendMessage"
          ],
          "Resource": "arn:aws:sqs:*:${local.account_id}:*"
        }
    ]
}
EOF



}



# # Lambda Permission
resource "aws_lambda_permission" "selenium_parser_apigw_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.selenium_lambda_function.lambda_function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${local.region}:${local.account_id}:${aws_api_gateway_rest_api.selenium_rest_api.id}/*/${aws_api_gateway_method.selenium_rest_api_parser_get.http_method}${aws_api_gateway_resource.selenium_rest_api_parser.path}"
}



resource "aws_lambda_permission" "selenium_parser_apigw_lambda_permission_2" {
  statement_id  = "AllowExecutionFromAPIGateway2"
  action        = "lambda:InvokeFunction"
  function_name = module.selenium_lambda_function.lambda_function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${local.region}:${local.account_id}:${aws_api_gateway_rest_api.selenium_rest_api.id}/*/${aws_api_gateway_method.selenium_rest_api_parse_html_post.http_method}${aws_api_gateway_resource.selenium_rest_api_parse_html.path}"
}


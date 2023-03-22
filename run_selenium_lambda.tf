module "submit_batch_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.environment}_submit_batch_job_lambda"
  description   = "Lambda function to submit batch job to run selenium automation"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  publish       = true
  memory_size   = 512
  timeout       = 900

  source_path = "./python/submit_batch_job_lambda/lambda_function.py"


  environment_variables = {
    JOB_DEFINITION   = aws_batch_job_definition.selenium_automation_job_definition.id
    JOB_QUEUE        = aws_batch_job_queue.selenium_automation_queue.arn
    SOURCE_S3_BUCKET = aws_s3_bucket.source_s3_bucket.id
    LOG_LEVEL        = "INFO"

  }

  allowed_triggers = {
    S3EventRule = {
      principal  = "events.amazonaws.com"
      source_arn = aws_cloudwatch_event_rule.s3_put_event_rule_output.arn
    }

  }

  attach_policy_json = true
  policy_json        = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "batch:DescribeJobQueues",
                "batch:DeregisterJobDefinition",
                "batch:DescribeJobs",
                "batch:ListTagsForResource",
                "batch:SubmitJob",
                "batch:DescribeSchedulingPolicies",
                "batch:RegisterJobDefinition",
                "batch:DescribeJobDefinitions",
                "batch:ListSchedulingPolicies",
                "batch:ListJobs",
                "batch:DescribeComputeEnvironments",
                "s3:*"
            ],
            "Resource": ["*"]
        }
    ]
}
EOF


}




##################
# Cloudwatch Resources
##################

##################################
# Cloudwatch Events (EventBridge)
##################################
resource "aws_cloudwatch_event_rule" "s3_put_event_rule_output" {
  name        = "s3-put-event-to-trigger-batch-job-lambda-rule"
  is_enabled  = true
  description = "S3 Put object event rule to invoke submit_batch_lambda_function"
  event_pattern = templatefile("${path.module}/policies/s3_put_event_pattern.json.tmpl",
    {
      S3_BUCKET_NAME = aws_s3_bucket.source_s3_bucket.id
  })

}

resource "aws_cloudwatch_event_target" "s3_put_event_lambda_function_target_output" {
  rule = aws_cloudwatch_event_rule.s3_put_event_rule_output.name
  arn  = module.submit_batch_lambda_function.lambda_function_arn
}

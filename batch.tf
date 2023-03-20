resource "aws_batch_compute_environment" "selenium_automation_batch" {
  compute_environment_name = "selenium_automation_batch_environmnet"

  compute_resources {
    max_vcpus = 16

    security_group_ids = [module.selenium_lambda_security_group.security_group_id]
    #    var.security_group_ids

    subnets = var.vpc_subnet_ids

    type = "FARGATE"
  }

  service_role = module.batch_iam_assumable_role.iam_role_arn
  type         = "MANAGED"
  depends_on   = []
}

resource "aws_batch_job_queue" "selenium_automation_queue" {
  name     = "selenium_automation_queue"
  state    = "ENABLED"
  priority = 99

  compute_environments = [
    aws_batch_compute_environment.selenium_automation_batch.arn
  ]
}

resource "aws_batch_job_definition" "selenium_automation_job_definition" {
  name = "selenium_automation_job_definition"
  type = "container"
  platform_capabilities = [
    "FARGATE",
  ]


  container_properties = <<CONTAINER_PROPERTIES
{
    "command": [
    ],
    "fargatePlatformConfiguration": {
      "platformVersion": "1.4.0"
    },
    "resourceRequirements": [
        {"type": "VCPU", "value": "1"},
        {"type": "MEMORY", "value": "2048"}
      ],
    "networkConfiguration": {
     "assignPublicIp": "ENABLED"
    },
    "image": "${module.selenium_ecr.repository_url}:latest",
    "jobRoleArn": "${aws_iam_role.ecs_task_execution_role.arn}",
    "executionRoleArn": "${module.ecs_task_iam_assumable_role.iam_role_arn}",
    "volumes": [],
    "environment": [

      {"name": "ARGS", "value": "{}"}

    ],
    "mountPoints": [],
    "ulimits": []
}
CONTAINER_PROPERTIES
}


resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.environment}_ecs_exec_role_${local.random_id}"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy_1" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy_2" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"

  #"arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
} # resource "aws_cloudwatch_event_rule" "batch_job_submit_rule" {
#   name        = "batch_job_submit_rule"
#   is_enabled  = true
#   description = "Rule to submit batch job"
#   role_arn    = module.batch_job_invoke_iam_assumable_role.iam_role_arn
#
#   event_pattern = templatefile("${path.module}/policies/s3_put_event_pattern.json.tmpl",
#     {
#       S3_BUCKET_NAME = aws_s3_bucket.output_s3_bucket.id
#   })
#
# }
#
# resource "aws_cloudwatch_event_target" "batch_job_submit_target" {
#   role_arn = module.batch_job_invoke_iam_assumable_role.iam_role_arn
#   rule     = aws_cloudwatch_event_rule.batch_job_submit_rule.name
#   arn      = aws_batch_job_queue.selenium_automation_queue.arn
#
#   batch_target {
#     job_name       = "test-submit-job"
#     job_definition = aws_batch_job_definition.selenium_automation_job_definition.id
#   }
#
#
#
#
#
# }
# resource "aws_batch_job_definition" "psql_maintenance_job_definition" {
#   name = "psql_maintenance_job_definition"
#   type = "container"
#   platform_capabilities = [
#     "FARGATE",
#   ]
#
#
#   container_properties = <<CONTAINER_PROPERTIES
# {
#     "command": [
#       "--help"
#     ],
#     "fargatePlatformConfiguration": {
#       "platformVersion": "1.4.0"
#     },
#     "resourceRequirements": [
#         {"type": "VCPU", "value": "1"},
#         {"type": "MEMORY", "value": "2048"}
#       ],
#     "networkConfiguration": {
#      "assignPublicIp": "ENABLED"
#     },
#     "image": "${module.selenium_ecr.repository_url}:latest",
#     "jobRoleArn": "${aws_iam_role.ecs_task_execution_role.arn}",
#     "executionRoleArn": "${module.ecs_task_iam_assumable_role.iam_role_arn}",
#     "volumes": [],
#     "environment": [
#
#       {"name": "DB_PORT", "value": "5432"},
#       {"name": "DB_NAME", "value": "REPLACE_ME"},
#       {"name": "SQL_FILE", "value": "REPLACE_ME"},
#       {"name": "COUNTY", "value": "REPLACE_ME"},
#       {"name": "STATE", "value": "REPLACE_ME"},
#       {"name": "S3_KEY", "value": "REPLACE_ME"}
#
#     ],
#     "mountPoints": [],
#     "ulimits": []
# }
# CONTAINER_PROPERTIES
# }

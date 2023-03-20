module "s3_bucket_code_build" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "code-build-s3-bucket-${random_id.random_id.hex}"
  acl    = "private"

  versioning = {
    enabled = false
  }



}


# CodeBuild
resource "aws_codebuild_project" "n8n_codebuild_project" {
  name          = "build-selenium"
  description   = "lorem ipsum"
  build_timeout = 60
  service_role  = module.codebuild_admin_iam_assumable_role.iam_role_arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_LARGE"
    image                       = "amazonlinux:2"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true

  }

  source {
    type = "NO_SOURCE"
    buildspec = templatefile("${path.module}/buildspec.yml.tmpl", {
      S3_BUCKET = module.s3_bucket_code_build.s3_bucket_id
    })
  }

  logs_config {
    cloudwatch_logs {
      group_name = module.codebuild_log_group.cloudwatch_log_group_name
    }
  }



}

module "codebuild_log_group" {
  source  = "terraform-aws-modules/cloudwatch/aws//modules/log-group"
  version = "3.0.0"

  name              = "codebuild_log_group_${random_id.random_id.hex}"
  retention_in_days = 7



}

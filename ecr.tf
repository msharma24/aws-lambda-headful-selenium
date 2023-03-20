module "selenium_ecr" {
  source  = "terraform-aws-modules/ecr/aws"
  version = "1.5.1"

  repository_name                 = "${var.environment}-selenium-ecr"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [data.aws_caller_identity.current.arn]
  create_lifecycle_policy           = true
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 30 images",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["v"],
          countType     = "imageCountMoreThan",
          countNumber   = 30
        },
        action = {
          type = "expire"
        }
      }
    ]
  })

  repository_force_delete = true

  #tags = local.tags
}

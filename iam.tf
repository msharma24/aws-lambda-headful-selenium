module "codebuild_admin_iam_assumable_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"
  version = "~> 4.5"

  trusted_role_services = [
    "codebuild.amazonaws.com"
  ]

  role_requires_mfa       = false
  create_role             = true
  create_instance_profile = true

  role_name = "codebuild-admin-role-${local.random_id}"

  custom_role_policy_arns = [
    "arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
  ]
}

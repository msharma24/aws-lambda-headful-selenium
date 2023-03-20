# Create zip-archive of a single directory where "pip install" will also be executed (default for python runtime with requirements.txt present)
# module "package_dir" {
#   source = "terraform-aws-modules/lambda/aws"
#
#   create_function = false
#
#   build_in_docker = true
#   runtime         = "python3.8"
#   source_path     = "${path.module}/python/"
#   artifacts_dir   = "${path.root}/builds/package_dir/"
# }
#
# output "file_name" {
#   value = module.package_dir.local_filename
# }

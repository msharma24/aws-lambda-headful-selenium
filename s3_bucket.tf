resource "aws_s3_bucket" "source_s3_bucket" {
  bucket = "${var.environment}-selenium-automation-source-${local.random_id}"
  acl    = "private"


  force_destroy = true # Prevents terraform destroy


  versioning {
    enabled = true
  }


}


resource "aws_s3_bucket_lifecycle_configuration" "source_s3_bucket" {

  bucket = aws_s3_bucket.source_s3_bucket.bucket
  rule {
    id     = "expiration-config"
    status = "Enabled"
    filter {}
    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}


resource "aws_s3_bucket" "cloudtrail_data_events" {
  bucket        = "${var.environment}-cloudtrail-${local.random_id}"
  force_destroy = true
}


resource "aws_cloudtrail" "cloudtrail_data_events" {
  name                          = "${var.environment}-deployment-cloudtrail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_data_events.id
  include_global_service_events = false

  depends_on = [aws_s3_bucket_policy.cloudtrail_data_events]

  event_selector {
    read_write_type           = "WriteOnly"
    include_management_events = true

    data_resource {
      type = "AWS::S3::Object"

      # Make sure to append a trailing '/' to your ARN if you want to monitor all objects in a bucket.
      values = [
        "${aws_s3_bucket.source_s3_bucket.arn}/Uploads/"
      ]
    }
  }
}


resource "aws_s3_bucket_policy" "cloudtrail_data_events" {
  bucket = aws_s3_bucket.cloudtrail_data_events.id

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:GetBucketAcl",
            "Resource": "${aws_s3_bucket.cloudtrail_data_events.arn}"
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:PutObject",
            "Resource": "${aws_s3_bucket.cloudtrail_data_events.arn}/AWSLogs/${local.account_id}/*",
            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
        }
    ]
}
POLICY

  depends_on = [
    aws_s3_bucket.cloudtrail_data_events
  ]

}


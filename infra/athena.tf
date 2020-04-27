provider "aws" {
  region                  = var.aws_region
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "Athena"
}

resource "aws_athena_workgroup" "this" {
  name = "athena_test"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.this.bucket}/outputs/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }
  }
  // Depends on the output location
  depends_on     = [aws_s3_bucket.this]
  tags = {
    Name = var.tag
  }
}

resource "aws_athena_database" "this" {
  name   = "test_db"
  bucket = aws_s3_bucket.this.bucket

  encryption_configuration {
    encryption_option = "SSE_S3"
  }
  depends_on     = [aws_s3_bucket.this, aws_athena_workgroup.this]
  // !For easy terraform destroy only
  force_destroy  = true
}

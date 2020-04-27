resource "aws_s3_bucket" "this" {
  bucket = "athena-showcase"
  region = var.aws_region
  // AES256 on Server Side
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  // !For easy terraform destroy only
  force_destroy = true
  tags = {
    Name = var.tag
  }
}
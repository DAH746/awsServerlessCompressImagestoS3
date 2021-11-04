/*
Terraform code to create a serverless Application to refactor an uploaded image

Creates two buckets: "source-image-bucket-5623" and "refactored-image-bucket-5623"

To Dos
Trigger lambda function from s3 events
Delete source picture when image is refactored - Maybe have a lifecycle instead of delete?
*/

provider "aws" {
 region = "eu-west-2"
}

// Creates the source image bucket
resource "aws_s3_bucket" "source-image-bucket" {
    bucket = "source-image-bucket-5623"
    acl = "private"

 versioning {
    enabled = true
 }
}

// Creates the refactored image bucket
resource "aws_s3_bucket" "refactored-image-bucket" {
    bucket = "refactored-image-bucket-5623"
    acl = "private"

 versioning {
    enabled = true
 }
}


// Testing s3 Trigger events for Lambda


// Creates IAM role for lambda 
resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

// Allows Lambda function to be invoked from S3 bucket
resource "aws_lambda_permission" "allow_source_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = // Function from Danyal
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source-image-bucket.arn
}

// Creates function from zip file
resource "aws_lambda_function" "func" {
  filename      = "your-function.zip"
  function_name = "example_lambda_name"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "exports.example"
  runtime       = "go1.x"
}

// Sets S3 notification when object is created in source bucket
// triggers lambda function
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.source-image-bucket.id

  lambda_function {
    lambda_function_arn = // Function from Danyal
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}
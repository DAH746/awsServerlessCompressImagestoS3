provider "aws" {
 region = "eu-west-2"
}

resource "aws_s3_bucket" "source-image-bucket" {
    bucket = "source-image-bucket-5623"
    acl = "private"

 versioning {
    enabled = true
 }
}

resource "aws_s3_bucket" "refactored-image-bucket" {
    bucket = "refactored-image-bucket-5623"
    acl = "private"

 versioning {
    enabled = true
 }
}
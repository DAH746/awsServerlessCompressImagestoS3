# awsServerlessCompressImagestoS3

<FILL LATER>

This project uses serverless architecture to resize an image uploaded to an S3
bucket.

As seen in the basic architecture diagram, the service works by a lambda function
being triggered by an S3 upload event. The lambda function then takes the file,
resizes it to 400x400 and uploads the picture to a seperate S3 bucket for the
resized images.

The image is named by using the version ID when uploaded to the source bucket 
and the name of the file uploaded. For example if the file name is picture.jpeg 
and the version ID given is XXXX, the new file name for the resized image would be:
picture_XXXX.jpeg


The buckets and lambda function are created using terraform, which gives these
services the correct permissions

For the resizing function to work PIL is required. This was utilised within the
project with the use of a lambda layer with the ARN "arn:aws:lambda:eu-west-2:770693421928:layer:Klayers-python38-Pillow:14".

Dependency list:
* json
    * boto3
    * PIL
    * io
    * os
    
Current Issues:
    * IAM policy for Lambda function to use S3 had to be created manually
    and attached via ARN in Terraform code.
    * Timeout of Lambda function is set at 3 seconds and is not changed via the
    timeout function in the Lambda function block even though this is set to 15s. This means that after the lambda function is created, the timeout has to be changed maunally on the aws management console to 15 seconds.
    

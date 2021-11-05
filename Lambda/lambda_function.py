# This file will compress the image that is uploaded
import json
import boto3 # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
from PIL import Image # Imports pillow image resizing functions
from io import BytesIO
import os

def lambda_handler (s3EventNotifcationAsJson, context):
    # event is expected to be the S3 bucket upload notification
    # https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
    
    s3EventNotifcationData = s3EventNotifcationAsJson['Records'][0]
    
    keyOfImageUploadedToS3 = s3EventNotifcationData['s3']['object']['key']
    
    bucketNameOfTheBucketTheImageWasUploadedTo = s3EventNotifcationData['s3']['bucket']['name']
    
    destinationBucketForRefactoredImage = "refactored-image-bucket-5623"
    
    objectRepresentingAnS3Bucket = boto3.client('s3')
    
    imageRawAsDict = objectRepresentingAnS3Bucket.get_object(Bucket = bucketNameOfTheBucketTheImageWasUploadedTo, Key = keyOfImageUploadedToS3)
    
    print(imageRawAsDict)
    
    imageRawAsStreamingBody = imageRawAsDict['Body'] # default file form u'Body': <botocore.response.StreamingBody object at 0x00000000042EDAC8>
    
    print(imageRawAsStreamingBody)
    
    imageRaw = BytesIO(imageRawAsStreamingBody.read())
    
    imageRaw = Image.open(imageRaw)
    
    print(imageRawAsDict['Body'].read())
    
    print(imageRaw)
    
    new_image = imageRaw.resize((400, 400))
    
    buffer= BytesIO()
    
    # file extention stuff
    fileNameSplit = keyOfImageUploadedToS3.split(".")
    fileName = fileNameSplit[0]
    fileExtention = fileNameSplit[1]
    
    if fileExtention.lower() == 'jpg' or 'jpeg':
        fileExtentionOfImageToBePassedToConverter = 'JPEG'
    elif fileExtention.lower() == 'png':
        fileExtentionOfImageToBePassedToConverter = 'PNG'
    else:
        raise Exception("Extention is NOT a JPG/JPEG OR PNG")
    # end - file extention stuff
    
    new_image.save(buffer, fileExtentionOfImageToBePassedToConverter)
    buffer.seek(0)

    # Apply unique filename
    uniqueVersionIDFromS3 = s3EventNotifcationData['s3']['object']['versionId']
    
    rebuildFileName = ""
    rebuildFileName += fileName# getting the filename without the extention
    rebuildFileName += "_" # underscore to signify the next segment
    rebuildFileName += uniqueVersionIDFromS3 # unique versionID from s3
    rebuildFileName += "." + fileExtention # .jpg or .png from earlier
    # End
    
    sent_data = objectRepresentingAnS3Bucket.put_object(Bucket=destinationBucketForRefactoredImage, Key=rebuildFileName, Body=buffer)
    
    
    print("REACHED END OF FILE")
    
    
# ------------- Example JSON for S3 notification, passed in as the "event" param
    
#     {
#   "Records": [
#     {
#       "eventVersion": "2.0",
#       "eventSource": "aws:s3",
#       "awsRegion": "us-east-1",
#       "eventTime": "1970-01-01T00:00:00.123Z",
#       "eventName": "ObjectCreated:Put",
#       "userIdentity": {
#         "principalId": "EXAMPLE"
#       },
#       "requestParameters": {
#         "sourceIPAddress": "127.0.0.1"
#       },
#       "responseElements": {
#         "x-amz-request-id": "C3D13FE58DE4C810",
#         "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
#       },
#       "s3": {
#         "s3SchemaVersion": "1.0",
#         "configurationId": "testConfigRule",
#         "bucket": {
#           "name": "sourcebucket",
#           "ownerIdentity": {
#             "principalId": "EXAMPLE"
#           },
#           "arn": "arn:aws:s3:::mybucket"
#         },
#         "object": {
#           "key": "Happy_Face.jpg",
#           "size": 1024,
#           "versionId": "version",
#           "eTag": "d41d8cd98f00b204e9800998ecf8427e",
#           "sequencer": "Happy Sequencer"
#         }
#       }
#     }
#   ]
# }

# ----------------- response from <boto3 s3 obj>.get_object:
#   RESPONSE AS DICT
# {
#     'Body': StreamingBody(),
#     'DeleteMarker': True|False,
#     'AcceptRanges': 'string',
#     'Expiration': 'string',
#     'Restore': 'string',
#     'LastModified': datetime(2015, 1, 1),
#     'ContentLength': 123,
#     'ETag': 'string',
#     'MissingMeta': 123,
#     'VersionId': 'string',
#     'CacheControl': 'string',
#     'ContentDisposition': 'string',
#     'ContentEncoding': 'string',
#     'ContentLanguage': 'string',
#     'ContentRange': 'string',
#     'ContentType': 'string',
#     'Expires': datetime(2015, 1, 1),
#     'WebsiteRedirectLocation': 'string',
#     'ServerSideEncryption': 'AES256'|'aws:kms',
#     'Metadata': {
#         'string': 'string'
#     },
#     'SSECustomerAlgorithm': 'string',
#     'SSECustomerKeyMD5': 'string',
#     'SSEKMSKeyId': 'string',
#     'BucketKeyEnabled': True|False,
#     'StorageClass': 'STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'GLACIER'|'DEEP_ARCHIVE'|'OUTPOSTS',
#     'RequestCharged': 'requester',
#     'ReplicationStatus': 'COMPLETE'|'PENDING'|'FAILED'|'REPLICA',
#     'PartsCount': 123,
#     'TagCount': 123,
#     'ObjectLockMode': 'GOVERNANCE'|'COMPLIANCE',
#     'ObjectLockRetainUntilDate': datetime(2015, 1, 1),
#     'ObjectLockLegalHoldStatus': 'ON'|'OFF'
# }

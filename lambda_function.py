import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
     
def resize_image(image_path, resized_path, sns_client):
    Topic_Arn = os.environ['Topic_Arn']
    with Image.open(image_path) as image:
        width, height = image.size
        new_width = width // 2
        new_height = height // 2
        resized_image = image.resize((new_width, new_height))
        resized_image.save(resized_path)
        print(image_path + " " + resized_path)
        message = f"The image {image_path} has been successfully resized."
        sns_client.publish(TopicArn=Topic_Arn, Message=message)

    
    
def handler(event, context):
    Topic_Arn = os.environ['Topic_Arn']
    S3_Bucket = os.environ['S3_Bucket']
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/RESIZED-{}'.format(key)
        
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path, sns_client)
        s3_client.upload_file(upload_path, S3_Bucket.format(bucket), key)

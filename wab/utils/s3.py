import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def connect_s3():
    client = boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )
    return client


def upload_to_s3(folder, file_name, file):
    s3 = connect_s3()
    bucket_name = settings.AWS_BUCKET_NAME
    region_name = settings.AWS_REGION_NAME
    bucket = s3.Bucket(bucket_name)
    path = f"{folder}/{file_name}"
    bucket.put_object(Key=path, Body=file, ACL='public-read', ContentType=file.content_type)
    url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, region_name, path)
    return url


def delete_s3(folder, file_name):
    s3 = connect_s3()
    bucket = s3.Bucket(settings.AWS_BUCKET_NAME)
    path = f"{folder}/{file_name}"
    return bucket.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': path
                }
            ]
        }
    )

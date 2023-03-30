import os
import logging
from logging import config
import boto3

import aws

ROOT_PATH = os.path.dirname(aws.__file__).removesuffix('aws')

config.fileConfig(os.path.join(ROOT_PATH, 'logger.conf'))
logger = logging.getLogger("aws.S3")


class S3:
    """Class responsible for S3 operations"""

    def __init__(self):
        try:
            self.resource = boto3.resource('s3')
            self.client = boto3.client('s3')
        except Exception:
            raise

    def delete_object(self, bucket_name: str, key: str) -> bool:
        """
        Deletes an object from bucket.

        :param bucket_name: Bucket that contains the object.
        :param key: Key of the object you want to delete.

        :return: True if the object was deleted, else it returns False.
        """

        try:
            bucket = self.resource.Bucket(bucket_name)
            bucket.Object(key).delete()
            logger.info(f'Successfully deleted s3://{bucket_name}/{key}')
            return True
        except Exception as e:
            logger.error(f'Failed delete s3://{bucket_name}/{key}. Error: {str(e)}')
            return False

    def upload_file(self, file_path: str, file_name: str, bucket_name: str,  object_key: str = None) -> bool:
        """
        Upload a file to a S3 bucket.

        :param str file_path: Folder path of the file to be uploaded.
        :param str file_name: File to be uploaded.
        :param str bucket_name: Bucket to upload to.

        :return: True if the file was uploaded, else False.
        """
        if object_key is None:
            object_key = file_name

        try:
            full_path = os.path.join(file_path, file_name)
            self.client.upload_file(full_path, bucket_name, object_key)
            logger.info(f'File {full_path} uploaded to {bucket_name}/{object_key}!')
            return True
        except Exception as e:
            logger.error(f'Failed upload {full_path} to {bucket_name}/{object_key} S3 Bucket. Error: {str(e)}')
            return False

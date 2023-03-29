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

    def upload_file(self):
        pass

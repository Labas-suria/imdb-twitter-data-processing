import os
import unittest
from unittest.mock import patch, Mock

from boto3.exceptions import ResourceNotExistsError
from botocore.exceptions import ConnectionError

import aws
from aws.s3 import S3

ROOT_PATH = os.path.dirname(aws.__file__).removesuffix('aws')

SERVICE_NAME = 's3'
WRONG_SERVICE_NAME = 's33'
AVAILABLE_SERVICES = ["s3", "ec2"]

BUCKET_NAME = 'my_bucket'
WRONG_BUCKET_NAME = 'non_existent_bucket'
OBJ_KEY = 'obj_key'

FILE_PATH = 'path/to/'
FILE_NAME = 'file.txt'


class TestS3Class(unittest.TestCase):

    @patch('boto3.resource')
    def test_s3_resource_creation(self, mock_resource):
        mock_resource.side_effect = ResourceNotExistsError(WRONG_SERVICE_NAME, AVAILABLE_SERVICES, True)
        self.assertRaises(Exception, S3, WRONG_SERVICE_NAME)

    @patch('boto3.client')
    def test_s3_client_creation(self, mock_client):
        mock_client.side_effect = ConnectionError(error='connection error')
        self.assertRaises(Exception, S3, WRONG_SERVICE_NAME)

    def test_delete_object(self):
        s3 = S3()
        with patch('boto3.resources.action.ServiceAction.__call__'):
            self.assertEqual(True, s3.delete_object(bucket_name=BUCKET_NAME, key=OBJ_KEY))

        with patch('boto3.resources.action.ServiceAction.__call__', side_effect=Exception('Any Exception')):
            with self.assertLogs() as captured:
                s3.delete_object(bucket_name=WRONG_BUCKET_NAME, key=OBJ_KEY)
                self.assertEqual(1, len(captured.records))
                self.assertEqual(captured.records[0].getMessage(),
                                 f'Failed delete s3://{WRONG_BUCKET_NAME}/{OBJ_KEY}. Error: Any Exception')

            self.assertEqual(False, s3.delete_object(bucket_name=WRONG_BUCKET_NAME, key=OBJ_KEY))

    def test_upload_file(self):
        s3 = S3()
        s3.client.upload_file = Mock()

        self.assertEqual(True, s3.upload_file(file_path=FILE_PATH, file_name=FILE_NAME, bucket_name=BUCKET_NAME))

        s3.client.upload_file.side_effect = Exception('Any Exception')
        full_path = os.path.join(FILE_PATH, FILE_NAME)
        with self.assertLogs() as captured:
            s3.upload_file(file_path=FILE_PATH,
                           file_name=FILE_NAME,
                           bucket_name=WRONG_BUCKET_NAME,
                           object_key=f'folder/{FILE_NAME}')

            self.assertEqual(1, len(captured.records))
            self.assertEqual(captured.records[0].getMessage(),
                             (f'Failed upload {full_path} to {WRONG_BUCKET_NAME}/folder/{FILE_NAME} S3 Bucket.'
                              ' Error: Any Exception'))

        self.assertEqual(False,
                         s3.upload_file(file_path=FILE_PATH, file_name=FILE_NAME, bucket_name=WRONG_BUCKET_NAME))

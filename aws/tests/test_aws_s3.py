import os
import unittest
from unittest.mock import patch, Mock

import boto3
from boto3.exceptions import ResourceNotExistsError

import aws
from aws.s3 import S3

ROOT_PATH = os.path.dirname(aws.__file__).removesuffix('aws')

SERVICE_NAME = 's3'
WRONG_SERVICE_NAME = 's33'
AVAILABLE_SERVICES = ["s3", "ec2"]

BUCKET_NAME = 'my_bucket'
WRONG_BUCKET_NAME = 'non_existent_bucket'
OBJ_KEY = 'obj_key'


class TestS3Class(unittest.TestCase):

    @patch('boto3.resource')
    def test_s3_resource_creation(self, mock_resource):
        mock_resource.side_effect = ResourceNotExistsError(WRONG_SERVICE_NAME, AVAILABLE_SERVICES, True)
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

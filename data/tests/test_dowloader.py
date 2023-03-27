import os
import typing
import unittest
from unittest.mock import patch, Mock
import requests

import data
from data.downloader import Downloader
from utils.mock_response import MockResponse

ROOT_PATH = os.path.dirname(data.__file__).removesuffix('data')

GOOD_DATA_SOURCE_SINGLE = {"file.txt": "https://path/txt"}
EXCEPT_DATA_SOURCE_SINGLE = {"file.txt": "https://path/timeout/txt"}
GOOD_DATA_SOURCE_MULTIPLE = {
    "file.txt": "https://path/txt",
    "file.csv": "https://path/csv"}


def mocked_requests_get(url, **kwargs):
    """Method responsible for simulating request.get method behaviors"""

    if url == 'https://path/txt':
        return MockResponse('txt', 200)
    if url == 'https://path/csv':
        return MockResponse('csv', 200)
    if url == 'https://path/timeout/txt':
        raise requests.exceptions.Timeout


class TestDownloaderClass(unittest.TestCase):

    def test_constructor(self) -> None:
        """Asserts the data_source can't be empty."""

        self.assertRaises(Exception, Downloader, data_source={})

    def test_download_default(self) -> None:
        """Asserts the download method works correctly when data will not be saved."""

        with patch('requests.get', side_effect=mocked_requests_get):
            exce_downloader = Downloader(EXCEPT_DATA_SOURCE_SINGLE)
            self.assertRaises(Exception, exce_downloader.download)

            downloader = Downloader(GOOD_DATA_SOURCE_SINGLE)
            returned = downloader.download()
            self.assertEqual(returned, {"response": {"file.txt": b"txt"}})
            self.assertEqual(bytes, type(returned["response"]["file.txt"]))

            downloader = Downloader(GOOD_DATA_SOURCE_MULTIPLE)
            returned = downloader.download()["response"]
            self.assertEqual(2, len(returned))

    def test_download(self) -> None:
        """Asserts the download method works correctly when data will be saved."""

        with patch('requests.get', side_effect=mocked_requests_get):

            with patch('builtins.open'):
                typing.BinaryIO.write = Mock()

                downloader = Downloader(GOOD_DATA_SOURCE_SINGLE, save_data=True, path_destin=r'folder\sub\folder')
                self.assertEqual(r'folder\sub\folder\file.txt', downloader.download()["response"]["file.txt"])

                expected = {
                    "file.txt": r"folder\sub\folder\file.txt",
                    "file.csv": r"folder\sub\folder\file.csv"
                }
                downloader = Downloader(GOOD_DATA_SOURCE_MULTIPLE, save_data=True, path_destin=r'folder\sub\folder')
                self.assertEqual(expected, downloader.download()["response"])

                downloader = Downloader(GOOD_DATA_SOURCE_SINGLE, save_data=True)
                self.assertEqual(os.path.join(ROOT_PATH, 'file.txt'), downloader.download()["response"]["file.txt"])

                expected = {
                    "file.txt": os.path.join(ROOT_PATH, 'file.txt'),
                    "file.csv": os.path.join(ROOT_PATH, 'file.csv')
                }
                downloader = Downloader(GOOD_DATA_SOURCE_MULTIPLE, save_data=True)
                self.assertEqual(expected, downloader.download()["response"])

            with patch('builtins.open', side_effect=Exception("Any Exception")):
                downloader = Downloader(GOOD_DATA_SOURCE_SINGLE, save_data=True)
                self.assertRaises(Exception, downloader.download)

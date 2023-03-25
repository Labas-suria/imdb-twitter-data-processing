import unittest


from data.downloader import Downloader


class TestDownloaderClass(unittest.TestCase):

    def test_downloader_constructor(self) -> None:
        self.assertRaises(Exception, Downloader, data_source={})
        self.assertRaises(Exception,
                          Downloader,
                          data_source={"key": "value"},
                          path_destin=None
                          )

    def test_download(self) -> None:
        #self.assertRaises()
        pass

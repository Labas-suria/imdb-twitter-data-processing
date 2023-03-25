
class Downloader:
    """Class responsible for download data from url and save data"""

    def __init__(self, data_source: dict, path_destin=None, save_data=False) -> None:
        """
        :param dict data_source: dict with the data names as keys and source url as values.
        :param str path_destin: path of folder where data will be saved if save_data is True.
        :param bool save_data: flag that determines if downloaded data will be saved to disk.
        """

        if len(data_source) == 0:
            raise Exception("data_source can't be empty")

        self.path_destin = path_destin
        self.data_url = data_source

    def download(self) -> dict:
        pass

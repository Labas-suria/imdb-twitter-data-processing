import os
import requests
import logging
from logging import config
import data

ROOT_PATH = os.path.dirname(data.__file__).removesuffix('data')

config.fileConfig(os.path.join(ROOT_PATH, 'logger.conf'))
logger = logging.getLogger("data.Downloader")


class Downloader:
    """Class responsible for download and save data from url"""

    def __init__(self, data_source: dict, path_destin: str = None, save_data: bool = False) -> None:
        """
        :param dict data_source: dict with the data names as keys and source url as values.
        :param str path_destin: a valid path of folder where data will be saved if save_data is True.
        :param bool save_data: flag that determines if downloaded data will be saved to disk.
        """

        if len(data_source) == 0:
            raise Exception("data_source can't be empty")

        self.path_destin = path_destin
        self.data_source = data_source
        self.save_data = save_data

    def download(self) -> dict:
        """
        Method responsible for download data determined in data_source and returns a dictionary with the
        file name as keys and file content in bytes as values.

        If save_data is true, the method will save the file in disk. Case path_destin has a valid path,
        the file will be saved there, case path_destin was None, the downloaded file will be saved in
        project root. So download method will return the dictionary with the file path instead the content in bytes.

        :return: a dictionary with the downloaded data, if save_data was true, or the saved data paths, if not.
        """

        source = self.data_source
        keys = source.keys()
        downloaded = {}

        for key in keys:
            file_name = key

            try:
                logger.info(f"Started downloading of {file_name}...")
                req_data = requests.get(source[key]).content
                logger.info(f"{file_name} download has finished.")
            except requests.exceptions.Timeout:
                logger.error(f"Failed download {file_name}. Timeout request")
                raise
            except requests.exceptions.TooManyRedirects:
                logger.error(f"Failed download {file_name}. Too many redirects")
                raise
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed download {file_name}. Error: {str(e)}")
                raise

            if self.save_data:

                file_path = os.path.join(ROOT_PATH, file_name)
                if self.path_destin is not None:
                    file_path = os.path.join(self.path_destin, file_name)

                try:
                    open(file_path, 'wb').write(req_data)
                    logger.info(f"{file_name} has been saved in {file_path}.")
                except Exception as e:
                    logger.error(f"Failed save {file_name} in disk. Error: {str(e)}")
                    raise

                downloaded[file_name] = file_path
            else:
                downloaded[file_name] = req_data

        return {"response": downloaded}

import os
import logging
from logging import config
from data.downloader import Downloader

import data

ROOT_PATH = os.path.dirname(data.__file__).removesuffix('data')

logging.config.fileConfig('logger.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')


def imdb_data_download():
    source = {"name.basics.tsv.gz": "https://datasets.imdbws.com/name.basics.tsv.gz"}
    downloader = Downloader(source, save_data=True)
    return downloader.download()


if __name__ == '__main__':
    imdb_data = imdb_data_download()

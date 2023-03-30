import logging
from logging import config

from aws.s3 import S3
from data.downloader import Downloader

logging.config.fileConfig('logger.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

IMDB_SOURCE = {
    "name.basics.tsv.gz": "https://datasets.imdbws.com/name.basics.tsv.gz",
    "title.basics.tsv.gz": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title.principals.tsv.gz": "https://datasets.imdbws.com/title.principals.tsv.gz"
}


if __name__ == '__main__':
    downloader = Downloader(IMDB_SOURCE, save_data=True)
    s3 = S3()
    

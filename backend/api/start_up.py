import sys
import os

def get_dir(folder_name):
    cwd = os.getcwd()
    basepath = ''
    while True:
        if os.path.exists(folder_name):
            break
        os.chdir('..')
        basepath = os.path.join(basepath, '..')
    os.chdir(cwd)
    if not basepath in sys.path:
        sys.path.insert(0, basepath)

get_dir("logger")
get_dir("data_cleaner")
get_dir("data_fetcher")

from logger.Logger import Logger
from data_cleaner.DataCleaner import DataCleaner
from data_fetcher.DataFetcher import DataFetcher

logger = Logger("logs_backend.db")
dataCleaner = DataCleaner("cleanData.db", "dirtyData.db")
fetcher = DataFetcher("dirtyData.db")


def start():
    logger.log("Server started", logger.urgency.LOW)
    fetcher.fetch_stock_data("..\..\data\stocks.csv")
    fetcher.close()

    # TODO update once datacleaner actually does what it is supposed to do
    # dataCleaner.verify_data()
    #logger.log("data structure verified", logger.urgency.LOW)

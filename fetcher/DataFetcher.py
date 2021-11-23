# import libraries
import pandas_datareader as pdr
import sqlite3
from datetime import datetime, timedelta 
import os
from logger.Logger import Logger

class DateFetcher:
    """
    A class designed to fetch data

    Params:

    """

    def __init__(self, db_name):
        assert type(db_name) is str and len(db_name) > 0, 'Database name must be provided as str'

        self.db_name = db_name
        self.logger = Logger('logs_data_fetcher.db')
        self._conn = None
        self._cursor = None
        self._connect()

    def connect(self):
        cwd = os.getcwd()
        data_dir = os.path.join(cwd, 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if self._conn is None:
            os.chdir(data_dir)
            self._conn = sqlite3.connect(self.db_name)
            self.logger.log(f'Created {self.db_name} in {data_dir}', self.logger.urgency.LOW)
        self._cursor = self._conn.cursor()
        os.chdir(cwd)

    def close(self):
        self.logger.log(f'Closing connection to {self.db_name}'. self.log)
        self._conn.close()
        self.logger.close()

    def fetch_stock_data(stock_file):

        with open(stock_file) as f:
            stocks = f.readlines()

        today = datetime.now() # todays date (YYYY-MM-DD HH:MM:SS)
        years = 10             # years back to start from
        startYear = today-timedelta(days=365*years)

        # fetch data for each stock
        for stock in stocks.list:
            df = pdr.DataReader(stock, data_source='yahoo', start=startYear, end=today)
            df.to_sql(stock, conn, if_exists='replace')
            print(df)
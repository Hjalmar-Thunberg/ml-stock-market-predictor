import pandas_datareader as pdr
import sqlite3
import csv
import os
from datetime import datetime, timedelta 
from logger.Logger import Logger
from tqdm import tqdm
class DataFetcher:
    """
    A class designed to fetch data

    Params:
        db_name: str - The database name where dirty data will be stored.
    """
    def __init__(self, db_name):
        assert type(db_name) is str and len(db_name) > 0, 'Database name must be provided as str'

        self.db_name = db_name
        self.logger = Logger('logs_data_fetcher.db')
        self._conn = None
        self._cursor = None
        self._connect()

    def _connect(self):
        """
        Connect to the specified database.
        Create a data directory if none exists.
        """
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
        """ Close database and logger connections """
        self.logger.log(f'Closing connection to {self.db_name}', self.logger.urgency.MODERATE)
        self._conn.close()
        self.logger.close()

    def fetch_all_stocks(self, stock_file):
        """ 
        Fetches given data from a csv file.
        Params:
            stock_file: The path to the input csv file.

        """
        with open(stock_file) as f:
            # Reads csv file into a list
            reader = csv.reader(f)
            stocks = list(reader)

            # fetch all data from yahoo for each given stock
            for stock in tqdm(stocks, position=0, leave=True):
                self.fetch_a_stock(stock[0])
    
    def fetch_a_stock(self, stock_name):
        """"
        Fetches given data from a specific stock name.
        Params:
            stock_name: The string name of a stock.
        """
        try:
            df = pdr.DataReader(stock_name, data_source='yahoo', start=datetime.now()-timedelta(days=365*10), end=datetime.now())
            df.columns = df.columns.str.replace(" ", "")
            df.to_sql(stock_name, self._conn, if_exists='replace')
            self.logger.log(f'Fetched data for {stock_name}', self.logger.urgency.LOW)
        except Exception as e:
            self.logger.log(f'{type(e)}: {e}, could not fetch data for {stock_name}', self.logger.urgency.HIGH) # TODO: this doesn't work
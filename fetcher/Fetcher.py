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
    """
    def __init__(self):

        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DATA_PATH = os.path.join(self.ROOT_DIR, 'data')
        self.cwd = os.getcwd()

        self.db_name = 'dirtyData.db'
        self.stock_file = 'stocks.csv'
        self.logger = Logger('logs_data_fetcher.db')
        self._conn = None
        self._cursor = None
        self._connect()

    def _connect(self):
        """
        Connect to the specified database.
        Create a data directory if none exists.
        """
        # Store the current working directory from the calling file
        # If the logs dir does not exist, create it
        if not os.path.exists(self.DATA_PATH) and self.cwd != self.DATA_PATH:
            os.mkdir(self.DATA_PATH)
            
        # If the current working dir is not ../logs change into it
        if self.cwd != self.DATA_PATH:
            os.chdir(self.DATA_PATH)
        
        # Establish a database connection if it does not exist
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_name, check_same_thread=False)
            #self.logger.log(f'Connected to {self.db_name} in {self.DATA_PATH}', self.logger.urgency.LOW)    
        
        # Create the cursor from the connection
        self._cursor = self._conn.cursor()
        # Change working directory back to cached working directory
        os.chdir(self.cwd)

    def close(self):
        """ Close database and logger connections """
        self.logger.log(f'Closing connection to {self.db_name}', self.logger.urgency.MODERATE)
        self._conn.close()
        self.logger.close()

    def fetch_all_stocks(self):
        """ 
        Fetches given data from a csv file.
        """
        os.chdir(self.DATA_PATH)
        with open(self.stock_file, 'r') as f:
            # Reads csv file into a list
            reader = csv.reader(f)
            stocks = list(reader)

            # fetch all data from yahoo for each given stock
            for stock in tqdm(stocks, position=0, leave=True, desc = 'Fetching stock data'):
                self.fetch_a_stock(stock[0])

        os.chdir(self.cwd)
        
    def fetch_a_stock(self, stock_name):
        """"
        Fetches given data from a specific stock name.
        """
        df = pdr.DataReader(stock_name, data_source='yahoo', start=datetime.now()-timedelta(days=365*10), end=datetime.now())
        df.columns = df.columns.str.replace(" ", "")
        if df is not None:
            df.to_sql(stock_name, self._conn, if_exists='replace')
            print(f'Fetched data for {stock_name}')
            self.logger.log(f'Fetched data for {stock_name}', self.logger.urgency.LOW)
        else: self.logger.log(f'could not fetch data for {stock_name}', self.logger.urgency.HIGH)
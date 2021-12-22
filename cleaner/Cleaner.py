import os
import sqlite3
import pandas as pd
from logger.Logger import Logger
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler

class DataCleaner:
    """
    A class designed to clean and validate data.
    """
    def __init__(self):
        
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DATA_PATH = os.path.join(self.ROOT_DIR, 'data')
        self.cwd = os.getcwd()

        # --- Database connections ---
        self.logger = Logger('logs_data_cleaner.db')
        self.clean_data_db = ('cleanData.db')
        self.dirty_data_db = ('dirtyData.db')
        self._conn_clean_db = None   # Clean database connection
        self._conn_dirty_db = None   # Dirty database connection
        self._cursor_clean_db = None # Clean database cursor
        self._cursor_dirty_db = None # Dirty database cursor
        self._connect()

        # --- Data preperations ---
        self.scaler = MinMaxScaler(feature_range=(0,1))

        # --- Verification Schemas ---
        self.STOCK_DATA_VERIFICATION_SCHEMA = ('Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'AdjClose')
        self.drop_out = ['High', 'Low', 'Open', 'Volume', 'AdjClose']

    def verify_data(self, dataframe, schema) -> bool:
        """
        Verifies if the given dataset matches the schema.
        Returns if dataset is valid or not.
        """
        is_valid = tuple(dataframe.columns) == schema
        if not is_valid:
            self.logger.log(f"{schema} verification failed for {tuple(dataframe.columns)}", self.logger.urgency.HIGH)
        return is_valid

    def _get_df_from_table(self, table_name, from_clean=False):
        """
        Searches in the dirtyData db for the specified table (table_name).
        Returns a dataframe of the table data.
        """
        conn = self._conn_dirty_db if not from_clean else self._conn_clean_db
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
        if df is not None:
            self.logger.log(f'Fetched dataframe from table {table_name}')
            return df
        else:
            self.logger.log(f'Failed to fetch {table_name}', self.logger.urgency.MODERATE)
        return None

    def get_all_cleaned_stocks(self):
        """ 
        Get stock names for all stocks stored in cleanData db.
        """
        cleaned_stocks = []
        self._cursor_clean_db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # Cache the tables from shared memory
        tables = self._cursor_clean_db.fetchall()
        # Iterate over each table
        for table in tables:
            cleaned_stocks.append(table[0])
        return cleaned_stocks    

    def clean_all_stocks(self):
        """ 
        Cleans data for all stocks stored in dirtyData db.
        Stores it in cleanedData db.
        """
        self._cursor_dirty_db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # Cache the tables from shared memory
        tables = self._cursor_dirty_db.fetchall()
        # Iterate over each table
        for table in tables:
            self.clean_a_stock(table[0])

    def clean_a_stock(self, stock_name):
        """
        Cleans data for a specific stock in the dirtyData db.
        Stores cleaned data in the cleanData db.
        """
        df = self._get_df_from_table(stock_name)
        if df is not None:
            print(f'Cleaning data for {stock_name}')
            df = df.drop(self.drop_out, axis=1)
            df['Close'].fillna(value=df['Close'].mean(), inplace=True) 
            df.to_sql(stock_name, self._conn_clean_db, if_exists='replace')
            self.logger.log(f'Cleaned data from table {stock_name}', self.logger.urgency.LOW)
        else:
            self.logger.log(f'Failed to clean {stock_name}', self.logger.urgency.MODERATE)

    def rescale_data(self, dataset):
        return self.scaler.inverse_transform(dataset)

    def get_prep_data(self, stock_name):
        """ Prepares and returns data to be used for trainer """
        df = self._get_df_from_table(stock_name, from_clean=True)
        
        # Create new dataframe with 'Close' column
        data_target = df.filter(['Close'])

        # Covert dataframe into a numpy array with a 1 day delay
        dataset = data_target.shift(-1, fill_value=0).values

        # Get the number of rows to train the model on, using 80% of the data
        training_data_len = math.ceil(len(dataset) * .9)

        # Scale data between 0 and 1 to avoid the bias using normalization
        
        scaled_data = self.scaler.fit_transform(dataset)

        # Create training dataset
        # Create the scaled training dataset
        train_data = scaled_data[0:training_data_len , :]

        # Create testing dataset
        # Create a new array containing scaled values
        time_interval = int(len(dataset)*0.05) # amount of steps to train on, I.E the amount of data the LSTM uses per "step" ex: [0,1,2....60] if time_interval = 10 first LSTM step will be 0-9 and predict 10, second step woule be 1-10 and predict 11. =
        test_data = scaled_data[training_data_len - time_interval: :]

        # Split data into x_train and y_train datasets
        x_train = []   # past x days, using previous example this would be 0-9
        y_train = []   # predicted target value.              this would be predicted value for 10

        # loop for the last x days
        for i in range(time_interval, len(train_data)):
            x_train.append(train_data[i-time_interval:i, 0]) # append closingprice for i day
            y_train.append(train_data[i, 0])             # append predicted value
            
        # Convert x_train and y_train to numpy arrays to use in LSTM model
        x_train, y_train = np.array(x_train), np.array(y_train)

        # Reshape data from 2D to 3D
        # LSTM network needs 3D input (number of samples, timesteps and features)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Create testing dataset
        # Create a new array containing scaled values
        test_data = scaled_data[training_data_len - time_interval: :]

        # Create the data sets x_test and y_test
        x_test = [] # past x days
        y_test = dataset[training_data_len:, :] # predicted value

        # loop for the last x days
        for i in range(time_interval, len(test_data)):
            x_test.append(test_data[i-time_interval:i, 0]) # append closing price for i day
            
        # Convert data into a numpy array to use in LSTM model
        x_test = np.array(x_test)

        # Reshape data from 2D to 3D
        # LSTM network needs 3D input (number of samples, timesteps and features)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        return x_train, y_train, x_test, y_test

    def _connect(self):
        """ 
        Connect to the specified databases.
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
        if self._conn_clean_db or self._conn_dirty_db is None:
            self._conn_clean_db = sqlite3.connect(self.clean_data_db, check_same_thread=False)
            self._conn_dirty_db = sqlite3.connect(self.dirty_data_db, check_same_thread=False)
            self.logger.log(f'Connected to {self.clean_data_db} in {self.DATA_PATH}', self.logger.urgency.LOW)
            self.logger.log(f'Connected to {self.dirty_data_db} in {self.DATA_PATH}', self.logger.urgency.LOW)   
        
        # Create the cursor from the connection
        self._cursor_clean_db = self._conn_clean_db.cursor()
        self._cursor_dirty_db = self._conn_dirty_db.cursor()
        # Change working directory back to cached working directory
        os.chdir(self.cwd)


    def close(self):
        """ Close database and logger connections """
        self.logger.log(f'Closing connection to {self.clean_data_db}', self.logger.urgency.MODERATE)
        self.logger.log(f'Closing connection to {self.dirty_data_db}', self.logger.urgency.MODERATE)
        self._conn_clean_db.close()
        self._conn_dirty_db.close()
        self.logger.close()
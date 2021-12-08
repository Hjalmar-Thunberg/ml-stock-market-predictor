import os
import sqlite3
import pandas as pd
from logger.Logger import Logger
class DataCleaner:
    """
    A class designed to clean and validate data.

    Params:
        clean_db_name: str - The database name where clean data will be stored.
        dirty_db_name: str - The dirty data database where the cleaner will fetch data from.
    """
    def __init__(self, clean_data_db, dirty_data_db):
        assert type(clean_data_db) is str and len(clean_data_db) > 0, 'Database name must be provided a str'
        assert type(dirty_data_db) is str and len(dirty_data_db) > 0, 'Database name must be provided a str'
        
        self.logger = Logger('logs_data_cleaner.db')
        self.clean_data_db = clean_data_db
        self.dirty_data_db = dirty_data_db
        self._conn_clean_db = None   # Clean database connection
        self._conn_dirty_db = None   # Dirty database connection
        self._cursor_clean_db = None # Clean database cursor
        self._cursor_dirty_db = None # Dirty database cursor
        self._connect()

        # --- Verification Schemas ---
        self.STOCK_DATA_VERIFICATION_SCHEMA = ('Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close')

    def verify_data(self, dataframe, schema) -> bool:
        """
        Verifies if the given dataset matches the schema.
        Returns if dataset is valid or not.
        """
        is_valid = tuple(dataframe.columns) == schema
        if not is_valid:
            self.logger.log(f"{schema} verification failed for {tuple(dataframe.columns)}", self.logger.urgency.HIGH)
        return is_valid

    def get_df_from_table(self, table_name):
        """
        Searches in the dirty data db for the specified table (table_name).
        Returns a dataframe of the table data.
        """
        try:
            df = pd.read_sql_query(f'SELECT * FROM {table_name}', self._conn_dirty_db)
            if df is not None:
                self.logger.log(f'Fetched dataframe from table {table_name}')
                return df
        except Exception as e:
            self.logger.log(f'{type(e)}: {e}', self.logger.urgency.HIGH)
        return None

    def _connect(self):
        """ 
        Connect to the specified databases.
        Create a data directory if none exists.
        """
        cwd = os.getcwd()
        data_dir = os.path.join(cwd, 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if self._conn_clean_db is None:
            os.chdir(data_dir)
            self._conn_clean_db = sqlite3.connect(self.clean_data_db)
            self._conn_dirty_db = sqlite3.connect(self.dirty_data_db)
            self.logger.log(f'Created {self.clean_data_db} in {data_dir}', self.logger.urgency.LOW)
            self.logger.log(f'Created {self.dirty_data_db} in {data_dir}', self.logger.urgency.LOW)
        self._cursor_clean_db = self._conn_clean_db.cursor()
        self._cursor_dirty_db = self._conn_dirty_db.cursor()
        os.chdir(cwd)

    def close(self):
        """ Close database and logger connections """
        self.logger.log(f'Closing connection to {self.clean_data_db}', self.logger.urgency.MODERATE)
        self.logger.log(f'Closing connection to {self.dirty_data_db}', self.logger.urgency.MODERATE)
        self._conn_clean_db.close()
        self._conn_dirty_db.close()
        self.logger.close()
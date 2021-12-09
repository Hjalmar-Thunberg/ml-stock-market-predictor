import os
import sqlite3
from datetime import datetime
from enum import Enum

class Logger:
    """
    A component used for logging events of other components.
    Designed to help increase readability of logs by allowing the user to
    customize their own event messages and specify an urgency.

    Params:
        database_name: str - The name the logger will use for the logs database file (e.g. "logs_scraper.db") .
    """
    def __init__(self, database_name):
        assert type(database_name) is str, 'Database name must be of type str'
        assert len(database_name) != 0, 'Database name must be provided to logger'

        # Urgency enum entrypoint
        self.urgency = self._Urgency
        # Today's date in the format Mon_DD_MM_YYYY
        self.today = datetime.now(tz=None).strftime('%a_%d_%b_%Y')
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.LOGS_PATH = os.path.join(self.ROOT_DIR, 'logs')
        self.cwd = os.getcwd()

        # Name of the database
        self.database_name = database_name

        # Database connection
        self._conn = None
        # Database cursor
        self._cursor = None
        self._connect()

    def _connect(self):
        """
        Establishes the connection and cursor to the database specified
        when instantiating the Logger.
        """
        # Store the current working directory from the calling file
        # If the logs dir does not exist, create it
        if not os.path.exists(self.LOGS_PATH) and self.cwd != self.LOGS_PATH:
            os.mkdir(self.LOGS_PATH)
            
        # If the current working dir is not ../logs change into it
        if self.cwd != self.LOGS_PATH:
            os.chdir(self.LOGS_PATH)
        
        # Establish a database connection if it does not exist
        if self._conn is None:
            self._conn = sqlite3.connect(self.database_name)
            
        # Create the cursor from the connection
        self._cursor = self._conn.cursor()
        # Change working directory back to cached working directory
        os.chdir(self.cwd)

    def log(self, message, urgency=None):
        """
        Log the given message to the database specified when creating
        the Logger. Urgency may be specified but is not required.

        Params:
            message: str - The message to log to the database.

            urgency: Logger._Urgency - The severity of the message.
                default value: Logger._Urgency.NONE
        """
        # Ensure the connection exists
        if not self._conn:
            self._connect()
           
        # Convert None value to Logger._Urgency.NONE
        if urgency is None:
            urgency = self.urgency.NONE
            
        # Query for creating a new table if it does not exist already
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.today} (
            timestamp,
            message,
            urgency
        )"""
            
        # Query for inserting the log into the table
        insert_log_query = f"""
        INSERT INTO {self.today} (timestamp, message, urgency)
        VALUES ('{self.get_timestamp()}', '{str(message)}', '{urgency.name}')
        """
        
        try:
            os.chdir(self.LOGS_PATH)
            # Execute the create table query
            self._cursor.execute(create_table_query)
            # Execute the insert log query
            self._cursor.execute(insert_log_query)
        except Exception as e:
            # Log any exceptions so that they may be dealt with in the future
            print(e)
        finally:
            # Commit changes
            self._conn.commit()
        os.chdir(self.cwd)

    def get_timestamp(self):
        """
        Get the current time as a timestamp in the format HH:MM:SS.MS (UTC).

        Returns:
            A string representing the timestamp.
        """
        # Create the timestamp in the format hours:minutes:seconds.microseconds
        return datetime.now(tz=None).strftime('%H:%M:%S.%f (UTC)')
    
    def close(self):
        """
        Closes the Logger's connection with the database.
        Only call this method when you are done with the Logger instance.
        """
        self._conn.close()
        
    class _Urgency(Enum):
        """
        A private enum class of the Logger component.
        Contains urgency levels along with a description of what
        the intended meaning is.
        """
        NONE     = 0 # Default value when urgency is not specified
        LOW      = 1 # Expected event or result
        MODERATE = 2 # Potentially unexpected event or result
        HIGH     = 3 # Caught exceptions, unexpected events
        SEVERE   = 4 # Exceptions that break the system, bugs, etc.

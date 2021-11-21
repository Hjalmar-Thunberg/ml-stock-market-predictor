# import libraries
import pandas_datareader as pdr
import sqlite3
import os
from datetime import datetime, timedelta 

 # fetcher attributes
stocks = ['GME', 'RBLX', 'NVDA', 'TSLA', 'COIN', 'FB', 'BYND', 'AAPL', 'AMC', 'MSFT', 'SHOP', 'ACB', 'TLRY', 'NFLX', 'GOOG', 'AMZN', 'DIS', 'BYND', 'ZM', 'PTON']
source = 'yahoo'
today = datetime.now() # todays date (YYYY-MM-DD HH:MM:SS)
years = 10             # years back to start from
startYear = today-timedelta(days=365*years)

# connect to sqlite database
conn = sqlite3.connect(os.path.realpath('../data/stock.db'))
c = conn.cursor()

# fetch data for each stock
for x in stocks:
    df = pdr.DataReader(x, data_source=source, start=startYear, end=today)
    df.to_sql(x, conn, if_exists='replace')
    print(df)


import pandas_datareader as pdr
import sqlite3

stocks = ['ETH-USD', 'TSLA', 'BTC-USD', 'BNB-USD', 'DIS', 'PSFE', 'BYND', 'SOFI', 'WISH', 'EGRNY', 'APP']
conn = sqlite3.connect("stocks.db")
c = conn.cursor()

for x in stocks:
    df = pdr.DataReader(x, data_source='yahoo', start='2005-01-01', end='2021-11-10')
    df.to_sql(x, conn, if_exists='replace')
    print(df)

for y in stocks:
    query = "SELECT * FROM " + y
    print(query)
    c.execute(query)

print(c.fetchone())

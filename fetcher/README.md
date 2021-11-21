# Fetcher Component
### Description
The fetcher is a component that will fetch that is being used for our system. It's primary objective is to collect stock data, including articles and social media trends that are related to any of these stocks or/ and companies. This is necessary for collecting a broad base of data.
### Requirements
- pandas_datareader
- sqlite3
### How to use
- pip3 install sqlite3 pandas_datareader
- cd to /fetcher folder
- python dataFetcher.py stock1 stock2 stock3... (no given stocks defaults to fetch top 19 most popular stocks)
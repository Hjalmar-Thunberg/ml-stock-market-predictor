# Fetcher Component
### Description
The fetcher is a component that will fetch that is being used for our system. It's primary objective is to collect stock data. This is necessary for collecting a broad base of data.

### Requirements

- pandas_datareader
- sqlite3

### How to setup:

`pip3 install sqlite3 pandas_datareader`

### How to run:

1. Import the Fetcher into the desired component. <br>
Due to the nature of importing modules from sibling directories a hacky approach is needed depending on the depth of the sibling dir.
```python
import sys
import os

cwd = os.getcwd()
basepath = ''
while True:
    if os.path.exists('fetcher'):
        break
    os.chdir('..')
    basepath = os.path.join(basepath, '..')
os.chdir(cwd)
if not basepath in sys.path:
    sys.path.insert(0, basepath)
from fetcher.Fetcher import fetcher
```

2. Create the Fetcher instance
```python
fetcher = DataFetcher('dirtyData.db')
```
3. Give the Fetcher a csv file path containing the stock names
```python
fetcher.fetch_stock_data('data/stocks.csv')
```

4. When the Fetcher is done, to preserve resources call:
```python
fetcher.close()
```

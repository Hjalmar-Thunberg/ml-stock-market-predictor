# Fetcher Component
### Description
The fetcher is a component that will fetch that is being used for our system. It's primary objective is to collect stock data. This is necessary for collecting a broad base of data.

### Requirements

- pandas_datareader
- sqlite3
- tqdm

### How to setup:

`pip3 install sqlite3 pandas_datareader tqdm`

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

2. Import the fetcher as a class
```python
import fetcher.Fetcher from DataFetcher
```

3. Create the Fetcher instance
```python
fetcher = DataFetcher()
```
4. Fetch either one stock or all saved ones by using one of the functions
```python
fetcher.fetch_a_stock('stock_name')
fetcher.fetch_all_stocks()
```

5. When the Fetcher is done, to preserve resources call:
```python
fetcher.close()
```

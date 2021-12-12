# Cleaner Component
### Description
The cleaner is a component that will clean dirty fetched data so it can be used by our model trainer. It's primary objective is to clean stock data. This is necessary for getting clean data to train on.

### Requirements

- pandas
- sqlite3
- numpy
- sklearn.preprocessing

### How to setup:

`pip3 install sqlite3 pandas numpy sklearn.preprocessing`

### How to run:

1. Import the Cleaner into the desired component. <br>
Due to the nature of importing modules from sibling directories a hacky approach is needed depending on the depth of the sibling dir.
```python
import sys
import os

cwd = os.getcwd()
basepath = ''
while True:
    if os.path.exists('cleaner'):
        break
    os.chdir('..')
    basepath = os.path.join(basepath, '..')
os.chdir(cwd)
if not basepath in sys.path:
    sys.path.insert(0, basepath)
from cleaner.Cleaner import DataCleaner
```

2. Create the Cleaner instance:
```python
cleaner = DataCleaner()
```
3. Clean either one or all saved stocks by using one of the functions:
```python
cleaner.clean_a_stock('stock_name')
cleaner.clean_all_stocks()
```

4. When the Cleaner is done, to preserve resources call:
```python
cleaner.close()
```

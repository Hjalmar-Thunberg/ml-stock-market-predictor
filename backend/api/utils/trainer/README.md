# Trainer Component
### Description
The trainer is a component that will train a model using cleaned data with Keras LSTM. It's primary objective is train models of different stocks. This is necessary for being able to predict future prices and changes.

### Requirements

- tensorflow
- keras

### How to setup:

`pip3 install tensorflow keras`

### How to run:

1. Import the Trainer into the desired component. <br>
Due to the nature of importing modules from sibling directories a hacky approach is needed depending on the depth of the sibling dir.
```python
import sys
import os

cwd = os.getcwd()
basepath = ''
while True:
    if os.path.exists('trainer'):
        break
    os.chdir('..')
    basepath = os.path.join(basepath, '..')
os.chdir(cwd)
if not basepath in sys.path:
    sys.path.insert(0, basepath)
from trainer.Trainer import Trainer
```

2. Create the Trainer instance:
```python
trainer = Trainer()
```
3. Train either one or all saved stocks by using one of the functions:
```python
trainer.train_a_stock('stock_name')
trainer.train_all_stocks()
```

4. When the Trainer is done, to preserve resources call:
```python
trainer.close()
```

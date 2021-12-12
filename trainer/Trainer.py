import math                                    # mathematical functions        https://docs.python.org/3/library/math.html
import pandas_datareader as web                # data reader for panda         https://pandas-datareader.readthedocs.io/en/latest/
import numpy as np                             # numerical data in python      https://numpy.org/doc/stable/user/absolute_beginners.html
import pandas as pd                            # data analysis toolkit         https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
import tensorflow.keras.backend as K
import matplotlib.pyplot as plt                # plotting data in figures      https://matplotlib.org/2.0.2/users/pyplot_tutorial.html
from sklearn.preprocessing import MinMaxScaler # raw data utility functions    https://scikit-learn.org/stable/modules/preprocessing.html
from keras import metrics as metrics
import tensorflow as tf
import sqlite3
import os
from cleaner.Cleaner import DataCleaner
from logger.Logger import Logger
from keras.models import Sequential            # input output sequence of data https://www.tensorflow.org/guide/keras/sequential_model
from datetime import datetime, timedelta       # for manipulating dates        https://docs.python.org/3/library/datetime.html
from keras.layers import Dense, LSTM, Dropout  # layers for neural network     https://keras.io/api/layers/

class Trainer:
    """"
    A class designed to train a model.
    """
    def __init__(self):

        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MODELS_PATH = os.path.join(self.ROOT_DIR, 'models')
        self.cwd = os.getcwd()
        
        self.logger = Logger('logs_model.db')

    def accuracy_calc(self, percentage, y_test, predictions):
        """ Calculates the accuracy of our predictions against the actual values within a given percentile """
        actual = y_test
        ok_accuracy = 0
        total = actual.size
        threshold = (100 - percentage) / 100
        lower = 1-threshold
        upper = 1+threshold

        for i in range(total):
            cur_act = actual[i]
            cur_pred = predictions[i]
            if cur_act >= cur_pred*lower and cur_act <= cur_pred*upper:
                ok_accuracy +=1
        acc = ok_accuracy/total
        print(f"Percentage of predicted values within {percentage}% margin of actual: {acc}")
        return acc

    def uniquify(self, path):
        """ Renames path name to a newer version if it already exists """
        
        if not os.path.exists(os.path.join(self.MODELS_PATH, path, '_v1')):
            return os.path.join(self.MODELS_PATH, path, '_v1')

        version_count = 1
        while os.path.exists(os.path.join(self.MODELS_PATH, path, '_v' + str(version_count))):
            version_count += 1

        return os.path.join(self.MODELS_PATH, path, '_v' + str(version_count))

    def train_all_stocks(self, num_nodes, save=False):
        """ 
        Train models using keras LSTM for all stocks in cleanData db.
        """
        cleaned_stocks = self.cleaner.get_all_cleaned_stocks()
        # Iterate over each table
        for stock_name in cleaned_stocks:
            self.train_a_stock(stock_name, num_nodes, save)    

    def train_a_stock(self, stock_name, num_nodes, save=False):
        """ 
        Trains a model using keras LSTM for a specific stock.
        Stores the model, prediction results and the accuracy in the models folder.
        """
        # Get training and testing data for a specific stock
        print(f'Training data for {stock_name}')
        x_train, y_train, x_test, y_test = self.cleaner.get_prep_data(stock_name)

        # Build LSTM model
        model = Sequential()

        # Run a layer with 500 nodes, drop 10% when done return whole output
        model.add(LSTM(num_nodes, return_sequences=False))
        model.add(Dropout(0.1))

        # Run a fourth layer with 25 nodes and 10% dropout
        model.add(Dense(25))
        model.add(Dropout(0.1))

        model.add(Dense(units = 1))

        # Method for calculating RMSE used for loss in model.compile
        def root_mean_squared_error(y_true, y_pred):
            return K.sqrt(K.mean(K.square(y_pred - y_true)))

        # Compile model
        # Optimizer is to improve upon the loss function https://keras.io/api/optimizers/adam/
        # loss function is used to measure how good the model did on training in terms of RMSE
        # Metrics is used to evaluate the accuracy of predicitons (currently does not work)
        model.compile(optimizer='adam', loss=root_mean_squared_error)

        # Train model
        # Batch size is the total number of training examples present in a single batch.
        # Epoch is the number of iterations when an entire dataset is passed forward and backward through a neural network
        model.fit(x_train, y_train, batch_size=48, epochs=10, validation_split=0.111)

        # Get model predicted unscaled closingprice value
        predictions = model.predict(x_test)
        predictions = self.cleaner.rescale_data(predictions)

        accs = []

        print("RMSE: ", root_mean_squared_error(y_test, predictions))
        accs.append(self.accuracy_calc(50, y_test, predictions))
        accs.append(self.accuracy_calc(60, y_test, predictions))
        accs.append(self.accuracy_calc(70, y_test, predictions))
        accs.append(self.accuracy_calc(80, y_test, predictions))
        accs.append(self.accuracy_calc(90, y_test, predictions))
        accs.append(self.accuracy_calc(95, y_test, predictions))
        accs.append(self.accuracy_calc(99, y_test, predictions))

        # Evaluate model 
        model.evaluate(x_test, y_test, batch_size=8)

        if save:
            # Saving Keras model
            path = self.uniquify(f'{stock_name}_lstm_model')

            model.save(path)

            os.chdir(path)

            with open(os.path.join(os.getcwd(), path, 'stats.txt'), 'w') as f:
                f.write('num_nodes: ' + str(num_nodes) + '\n')

                for acc in accs:
                    f.write('acc: ' + str(acc) + '\n')

                for pred in predictions:
                    f.write('pred: ' + str(pred[0]) + '\n')

            os.chdir(self.cwd)
            self.logger.log(f'Trained model for {stock_name}, stored in {path}')

        return accs
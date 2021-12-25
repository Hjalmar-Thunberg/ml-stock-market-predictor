from django import forms
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from models.models import PredictionModel
import sqlite3
import numpy as np
import pandas as pd
import os
import sys
import plotly
import plotly.express as px
import tensorflow as tf
from tensorflow import keras


def get_dir(folder_name):
    cwd = os.getcwd()
    basepath = ""
    while True:
        if os.path.exists(folder_name):
            break
        os.chdir("..")
        basepath = os.path.join(basepath, "..")
    os.chdir(cwd)
    if not basepath in sys.path:
        sys.path.insert(0, basepath)


get_dir("logger")
get_dir("cleaner")
get_dir("fetcher")
get_dir("trainer")

from logger.Logger import Logger
from cleaner.Cleaner import DataCleaner
from fetcher.Fetcher import DataFetcher
from trainer.Trainer import Trainer

logger = Logger("logs_backend.db")
cleaner = DataCleaner()
fetcher = DataFetcher()
trainer = Trainer()

CWD = os.getcwd()
ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
MODELS_DIR = os.path.join(ROOT_DIR, "models")
PREDICTIONS_DIR = os.path.join(ROOT_DIR, "data")
# { 'AAPL': 'Path/to/apple/_v1'}
models_in_use = {}


def get_all_stock_model_versions_data(stock_symbol) -> list:
    model_data = []
    folder = list(
        filter(
            lambda folder_name: folder_name.split("_")[0] == stock_symbol,
            os.listdir(MODELS_DIR),
        )
    )[0]
    for version in os.listdir(os.path.join(MODELS_DIR, folder)):
        model_data.append(get_stock_model_data(stock_symbol, version=int(version[2:])))
    return JsonResponse(model_data, safe=False, status=200)


def get_stock_model_data(stock_symbol, version: int = 0) -> tuple:
    mv, nn = 0, 0
    a, p = [], []
    folder = list(
        filter(
            lambda folder_name: folder_name.split("_")[0] == stock_symbol,
            os.listdir(MODELS_DIR),
        )
    )[0]
    if folder.split("_")[0] == stock_symbol:
        model_version = sorted(
            os.listdir(os.path.join(MODELS_DIR, folder)), key=lambda ver: int(ver[2:])
        )[version - 1]
        mv = int(model_version[2:])
        stats_path = os.path.join(MODELS_DIR, folder, model_version, "stats.txt")
        with open(stats_path, "r") as f:
            for line in f.readlines():
                ls = line.split(" ")
                if ls[0].startswith("num"):
                    nn = int(ls[1])
                if ls[0].startswith("acc"):
                    a.append(round(float(ls[1]), 6) * 100)
                if ls[0].startswith("pred"):
                    p.append(round(float(ls[1]), 2))

        return tuple([mv, nn, a, p])

def get_dropdown_options():
    return tuple([(key, key) for key in list(models_in_use.keys())])


class StocksDropdownForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StocksDropdownForm, self).__init__(*args, **kwargs)
        self.fields["stocks"] = forms.ChoiceField(choices=get_dropdown_options())


def populate_dropdown():
    with open(os.path.join(PREDICTIONS_DIR, "models_in_use.txt"), "r") as f:
        for pair in f.readlines():
            (key, value) = pair.split("=")
            models_in_use[key] = value


def index(request):
    populate_dropdown()
    form = StocksDropdownForm()
    if request.method == "POST":
        form = StocksDropdownForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data["stocks"]
            return HttpResponseRedirect(f"http://localhost:8000/get-pred/{stock}")
    errors = form.errors or None
    return render(request, "index.html", {"form": form, "errors": errors})


def get_model_in_use_path(stock):
    with open(os.path.join(PREDICTIONS_DIR, "models_in_use.txt"), "a+") as f:
        f.seek(0)
        for line in f.readlines():
            if stock in line:
                return line.split("=")[1]
    return ""


def get_model_path(stock_symbol: str, version=0) -> str:
    if version < 0:
        raise IndexError("Model version must be >= 0")
    folder = list(
        filter(
            lambda folder_name: folder_name.split("_")[0] == stock_symbol,
            os.listdir(MODELS_DIR),
        )
    )
    if folder:
        folder = folder[0]
        model_version = sorted(
            os.listdir(os.path.join(MODELS_DIR, folder)), key=lambda ver: int(ver[2:])
        )[version - 1]
        model_path = os.path.join(MODELS_DIR, folder, model_version)
        return model_path
    return ""


# This should run every 24 hours and have option for force refresh
def prepare_daily_data():
    fetcher.fetch_all_stocks()
    cleaner.clean_all_stocks()


def get_pred(request, stock_symbol):
    fetcher.fetch_a_stock(stock_symbol)
    cleaner.clean_a_stock(stock_symbol)
    x_train, y_train, x_test, y_test = cleaner.get_prep_data(stock_symbol)
    if stock_symbol in models_in_use.keys():
        model_path = get_model_in_use_path(stock_symbol).strip()
        current_model = tf.keras.models.load_model(model_path, compile=False)
        to_predict = x_test
        predictions = current_model.predict(to_predict)

        version = int(get_model_in_use_path(stock_symbol).split("_")[-1][1:])
        mv, nn, a, p = get_stock_model_data(stock_symbol, version)
        p = [pred[0] for pred in cleaner.rescale_data(predictions)][-100:]
        actual_values = cleaner._get_df_from_table(stock_symbol, True)
        actual_values = actual_values["Close"][-len(p) :].tolist()
        df = pd.DataFrame(p, index=list(range(0, len(p))), columns=["Predicted Close"])
        df["Actual Close"] = actual_values
        fig = px.line(
            df,
            markers=True,
        )
        fig.update_layout(
            title={
                "text": "Our Predictions vs Actual",
				'x': 0.5,
				'y': 0.9,
                "xanchor": "center",
                "yanchor": "top",
            }
        )
        fig.update_xaxes(title_text="Last 100 Days")
        fig.update_yaxes(title_text="Closing Price")
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")

        context = {
            "prediction": round(p[-1], 2),
            "stock": stock_symbol,
            "model_version": mv,
            "num_nodes": nn,
            "acc_0": a[0],
            "acc_1": a[1],
            "acc_2": a[2],
            "acc_3": a[3],
            "acc_4": a[4],
            "acc_5": a[5],
            "acc_6": a[6],
            "graph_div": graph_div,
        }

        predictions = [
            f"{str(round(pred[0], 2))}" for pred in cleaner.rescale_data(predictions)
        ]
        str_preds = "\n".join(predictions)
        os.chdir(PREDICTIONS_DIR)
        conn = sqlite3.connect("user_predictions.db", check_same_thread=False)
        curs = conn.cursor()
        create_table_query = f"""
			CREATE TABLE IF NOT EXISTS {stock_symbol} (
			timestamp,
			predictions
		)"""

        insert_into_table_query = f"""
			INSERT INTO {stock_symbol} (timestamp, predictions)
			VALUES ('{logger.get_timestamp()}', '{str_preds}')
		"""

        try:
            curs.execute(create_table_query)
            curs.execute(insert_into_table_query)
        except Exception as e:
            logger.log(f"{type(e)}: {e}", logger.urgency.HIGH)
        finally:
            conn.commit()
            conn.close()
        os.chdir(CWD)

        return render(request, "predictions.html", context)
    else:
        return HttpResponseRedirect('http://localhost:8000')


def should_update_model_in_use_if_it_is_much_better_or_not_as_good(
    stock_symbol: str, model_acc: list
) -> bool:
    if get_model_path(stock_symbol) == "":
        return True
    cur_model_acc = get_stock_model_data(
        stock_symbol, int(models_in_use.get(stock_symbol).split(os.sep)[-1][2:])
    )[2]
    return [model_acc[i] >= cur_model_acc[i] for i in range(len(cur_model_acc))]


# Add model to list of in-use models if doesnt exist
def add_to_models_in_use(stock_symbol):
    model_path = os.path.join(MODELS_DIR, stock_symbol + "_lstm_model", "_v1")
    with open(os.path.join(PREDICTIONS_DIR, "models_in_use.txt"), "a+") as f:
        f.seek(0)
        models_in_use[stock_symbol] = model_path
        to_write = f"{stock_symbol}={model_path}\n"
        if stock_symbol not in [line.split("=")[0] for line in f.readlines()]:
            f.write(to_write)


# Update existing model version in list of in-use models
def update_model_in_use(stock_symbol, path_to_new_model):
    a = open(os.path.join(PREDICTIONS_DIR, "models_in_use.txt"), "a+")
    a.seek(0)
    lines = a.readlines()
    a.close()

    for line in lines:
        if line.split("=")[0] == stock_symbol:
            lines.pop(lines.index(line))

    b = open(os.path.join(PREDICTIONS_DIR, "models_in_use.txt"), "w+")
    b.seek(0)
    for line in lines:
        b.write(line)
    to_write = f"{stock_symbol}={path_to_new_model}\n"
    b.write(to_write)
    b.close()


def _admin_train(stock_symbol, num_nodes):
    trainer.train_a_stock(stock_symbol, int(num_nodes), True)
    add_to_models_in_use(stock_symbol)
    return HttpResponseRedirect(f"http://localhost:8000/get-pred/{stock_symbol}")


def admin_train(request, stock_symbol, num_nodes, should_save=False):
    save = True if should_save == "True" else False
    # Training on a new stock symbol that doesnt exist
    model_stats = trainer.train_a_stock(stock_symbol, int(num_nodes), save)
    responseMSG = True  # json.dumps(should_update_model_in_use_if_it_is_much_better_or_not_as_good(stock_symbol, model_stats['accuracy']))
    # update current model to be newly trained one
    if save == True:
        if get_model_in_use_path(stock_symbol) == "":
            add_to_models_in_use(stock_symbol)
            accuracies = model_stats['accuracy']
            model_version = '1'
            model_path = get_model_path(stock_symbol, int(model_version))
            pm = PredictionModel(
                for_stock=stock_symbol,
                acc_50=accuracies[0] * 100,
                acc_60=accuracies[1] * 100,
                acc_70=accuracies[2] * 100,
                acc_80=accuracies[3] * 100,
                acc_90=accuracies[4] * 100,
                acc_95=accuracies[5] * 100,
                acc_99=accuracies[6] * 100,
            )
            pm.VERSIONS.append(tuple([model_version]*2))
            pm.PATH_CHOICES.append((model_version, model_path))
            pm.version = model_version
            pm.path = model_path
            pm.save()
        else:
            update_model(request, stock_symbol, get_stock_model_data(stock_symbol)[0])

    return JsonResponse(responseMSG, safe=False, status=200)


def update_model(request, stock_symbol, version):
    file_path = get_model_path(stock_symbol, int(version))
    update_model_in_use(stock_symbol, file_path)
    return JsonResponse({}, status=200)


def admin_models(request, stock_symbol):
    # if request.method == "GET":

    print("it works wooho admin_models  ", stock_symbol)
    return JsonResponse({}, status=200)

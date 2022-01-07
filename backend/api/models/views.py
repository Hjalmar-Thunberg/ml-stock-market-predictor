from django import forms
from django.core.exceptions import ObjectDoesNotExist
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


def get_dir(folder_name):
    cwd = os.getcwd()
    print("my current dir: ",cwd)
    basepath = ""
    while True:
        if os.path.exists(os.path.join("utils",folder_name)):
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

from utils.logger.Logger import Logger
from utils.cleaner.Cleaner import DataCleaner
from utils.fetcher.Fetcher import DataFetcher
from utils.trainer.Trainer import Trainer

logger = Logger("logs_backend.db")
cleaner = DataCleaner()
fetcher = DataFetcher()
trainer = Trainer()

CWD = os.getcwd()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS_DIR = os.path.join(ROOT_DIR, "utils/models")
PREDICTIONS_DIR = os.path.join(ROOT_DIR, "utils/data")

class StocksDropdownForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dropdown_options = tuple([(model.for_stock, model.for_stock) for model in list(PredictionModel.objects.all())])
        super(StocksDropdownForm, self).__init__(*args, **kwargs)
        self.fields["stocks"] = forms.ChoiceField(choices=dropdown_options)

def get_all_stock_model_versions_data(request, stock_symbol) -> list:
    model_data = []
    folder = list(
        filter(
            lambda folder_name: folder_name.split("_")[0] == stock_symbol,
            os.listdir(MODELS_DIR),
        )
    )[0]
    for version in os.listdir(os.path.join(MODELS_DIR, folder)):
        model_data.append(get_stock_model_data(stock_symbol, version=int(version[2:])))
    response = {
        "model_data": model_data
    }
    return JsonResponse(response, status=200)


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

def index(request):
    form = StocksDropdownForm()
    if request.method == "POST":
        form = StocksDropdownForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data["stocks"]
            return HttpResponseRedirect(f"http://localhost:8000/get-pred/{stock}")
    errors = form.errors or None
    return render(request, "index.html", {"form": form, "errors": errors})


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

def load():
    return render("loading.html")

def get_pred(request, stock_symbol):
    fetcher.fetch_a_stock(stock_symbol)
    cleaner.clean_a_stock(stock_symbol)
    x_train, y_train, x_test, y_test = cleaner.get_prep_data(stock_symbol)
    existing_model = None
    try:
        existing_model = PredictionModel.objects.get(for_stock__iexact=stock_symbol)
    except ObjectDoesNotExist:
        HttpResponseRedirect(f"http://localhost:8000/train/{stock_symbol}/100/True")

    if existing_model:
        version = existing_model.version
        model_path = get_model_path(stock_symbol, version)
        current_model = tf.keras.models.load_model(model_path, compile=False)
        predictions = current_model.predict(x_test)

        p = get_stock_model_data(stock_symbol, version)[3]
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
            "stock": existing_model.for_stock,
            "model_version": version,
            "num_nodes": existing_model.num_nodes,
            "acc_0": existing_model.acc_50,
            "acc_1": existing_model.acc_60,
            "acc_2": existing_model.acc_70,
            "acc_3": existing_model.acc_80,
            "acc_4": existing_model.acc_90,
            "acc_5": existing_model.acc_95,
            "acc_6": existing_model.acc_99,
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
        load()
        return HttpResponseRedirect(f"http://localhost:8000/train/{stock_symbol}/100/True")


def should_update_model(stock_symbol: str, model_acc: list) -> bool:
    if get_model_path(stock_symbol) == "":
        return True
    model = PredictionModel.objects.get(for_stock__iexact=stock_symbol)
    cur_model_acc = [model.acc_50, model.acc_60, model.acc_70, model.acc_80, model.acc_90, model.acc_95, model.acc_99]
    return [model_acc[i] >= cur_model_acc[i] for i in range(len(cur_model_acc))]


def model_exists(stock_symbol) -> bool:
    try:
        model = PredictionModel.objects.get(for_stock__iexact=stock_symbol)
        return model != None
    except ObjectDoesNotExist:
        return False

# For admin use only
def _admin_model_train(stock_symbol, num_nodes):
    model_stats = trainer.train_a_stock(stock_symbol, num_nodes, True)
    # update current model to be newly trained one
    accuracies = model_stats['accuracy']
    model_version = get_stock_model_data(stock_symbol)[0]
    model_path = get_model_path(stock_symbol, int(model_version))
    pm = PredictionModel.objects.get(for_stock__iexact=stock_symbol)
    pm.acc_50 = accuracies[0] * 100
    pm.acc_60 = accuracies[1] * 100
    pm.acc_70 = accuracies[2] * 100
    pm.acc_80 = accuracies[3] * 100
    pm.acc_90 = accuracies[4] * 100
    pm.acc_95 = accuracies[5] * 100
    pm.acc_99 = accuracies[6] * 100
    pm.num_nodes = num_nodes
    pm.version = model_version
    pm.path = model_path
    pm.save()

def admin_train(request, stock_symbol, num_nodes, should_save=False):
    save = True if should_save == "True" else False
    # Training on a new stock symbol that doesnt exist
    model_stats = trainer.train_a_stock(stock_symbol, int(num_nodes), save)
    # update current model to be newly trained one
    if save == True:
        if not model_exists(stock_symbol):
            accuracies = model_stats['accuracy']
            model_version = 1
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
            pm.num_nodes = num_nodes
            pm.version = model_version
            pm.save()
        else:
            accuracies = model_stats['accuracy']
            model_version = get_stock_model_data(stock_symbol)[0]
            pm = PredictionModel.objects.get(for_stock__iexact=stock_symbol)
            pm.acc_50 = accuracies[0] * 100
            pm.acc_60 = accuracies[1] * 100
            pm.acc_70 = accuracies[2] * 100
            pm.acc_80 = accuracies[3] * 100
            pm.acc_90 = accuracies[4] * 100
            pm.acc_95 = accuracies[5] * 100
            pm.acc_99 = accuracies[6] * 100
            pm.num_nodes = num_nodes
            pm.version = model_version
            pm.save()

        return HttpResponseRedirect(f"http://localhost:8000/get-pred/{stock_symbol}")
    response = {
        "should_update": should_update_model(stock_symbol, model_stats['accuracy']),
        # "accuracy": list(model_stats['accuracy']),
        # "predictions": list(model_stats['predictions'])
        }
    return JsonResponse(response, status=200)
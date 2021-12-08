from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status, permissions
from .models import PredModel
from .serializers import Serializer
import sqlite3
import os
import pandas as pd
import json

# class JSONResponse(HttpResponse):
# 	def __init__(self, data, **kwargs):
# 		content = JSONRenderer().render(data)
# 		kwargs['content_type'] = 'application/json'
# 		super(JSONResponse, self).__init__(content, **kwargs)

# class IsAuthenticated(permissions.IsAuthenticated):
# 	def has_permission(self, request, view):
# 		if request.method == 'OPTIONS':
# 			return True
# 		return super(IsAuthenticated, self).has_permission(request, view)

def get_pred(request, table_name):
	print("it works wooho get_pred      ", table_name)
	return HttpResponse(status=status.HTTP_200_OK)

def admin_train(request, stock_symbol):
	print("it works wooho  admin_train  ", stock_symbol)
	return HttpResponse(status=status.HTTP_200_OK)

def admin_models(request, stock_symbol):
	print("it works wooho admin_models  ", stock_symbol)
	return HttpResponse(status=status.HTTP_200_OK)

def test(request):
	pass

def get_df_from_table(table_name):
	"""
	Searches in the dirty data db for the specified table (table_name).
	Returns a dataframe of the table data.
	"""
	database_path = os.path.abspath('../../data/dirtyData.db')
	conn = sqlite3.connect(database_path)
	df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
	if df is not None:
		return df
	return None

def get_model_data(request, table_name):
	print(request)
	if request.method == "OPTIONS":
		return HttpResponse(status=status.HTTP_200_OK)

	if request.method == "GET":
		print(table_name)
		stock_data = get_df_from_table(table_name)
		stock_data = stock_data.to_json()
		return JsonResponse(json.loads(stock_data), safe=False, status=status.HTTP_200_OK)

# api calls for get/post no key req
# for prediction models using python objects 
@csrf_exempt
def task_list(request):
	if request.method == 'GET':
		task = PredModel.objects.all()
		task_serializer = Serializer(task, many=True)
		return JsonResponse(task_serializer.data)

	elif request.method == 'POST':
		task_data = JSONParser().parse(request)
		task_serializer = Serializer(data=task_data)
		if task_serializer.is_valid():
			task_serializer.save()
			return JsonResponse(task_serializer.data, \
								status=status.HTTP_201_CREATED)
		return JsonResponse(task_serializer.errors, \
							status = status.HTTP_400_BAD_REQUEST)
			
# api calls for get/put/delete with pk "private key"
# for prediction models using python objects
@csrf_exempt
def task_detail(request, pk):
	try: # cheks predmodel.objects for a specific instance
		task = PredModel.objects.get(pk=pk)
	except PredModel.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		task_serializer = Serializer(task, many=False)
		return JsonResponse(task_serializer.data)

	elif request.method == 'PUT':
		task_data = JSONParser().parse(request)
		task_serializer = Serializer(task, data=task_data)
		if task_serializer.is_valid():
			task_serializer.save()
			return JsonResponse(task_serializer.data)
		return JsonResponse(task_serializer.errors, \
							status=status.HTTP_400_BAD_REQUESTS)

	elif request.method == 'DELETE':
		task.delete()
		return HttpResponse(status=status.HTTP_204_NO_CONTENT)


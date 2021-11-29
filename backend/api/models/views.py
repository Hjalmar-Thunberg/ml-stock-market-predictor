from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import PredModel
from .serializers import Serializer


class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def task_list(request):
	if request.method == 'GET':
		task = PredModel.objects.all()
		task_serializer = Serializer(task, many=True)
		return JSONResponse(task_serializer.data)

	elif request.method == 'POST':
		task_data = JSONParser().parse(request)
		task_serializer = Serializer(data=task_data)
		if task_serializer.is_valid():
			task_serializer.save()
			return JSONResponse(task_serializer.data, \
								status=status.HTTP_201_CREATED)
		return JSONResponse(task_serializer.errors, \
							status = status.HTTP_400_BAD_REQUEST)
			

@csrf_exempt
def task_detail(request, pk):
	try:
		task = PredModel.objects.get(pk=pk)
	except PredModel.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		task_serializer = Serializer(task, many=False)
		return JSONResponse(task_serializer.data)

	elif request.method == 'PUT':
		task_data = JSONParser().parse(request)
		task_serializer = Serializer(task, data=task_data)
		if task_serializer.is_valid():
			task_serializer.save()
			return JSONResponse(task_serializer.data)
		return JSONResponse(task_serializer.errors, \
							status=status.HTTP_400_BAD_REQUESTS)

	elif request.method == 'DELETE':
		task.delete()
		return HttpResponse(status=status.HTTP_204_NO_CONTENT)
		

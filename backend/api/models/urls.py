# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers
from django.conf.urls import url
from . import views
  
# import everything from views
from .views import *
  
# define the router
router = routers.DefaultRouter()
  
# define the router path and viewset to be used
# router.register(r'models', ViewSet)
  
# specify URL Path for rest_framework
urlpatterns = [
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls'))
    url(r'^predModels/$',views.task_list),
    url(r'^test/$',views.test),
    url(r'^get-model-data/(?P<table_name>\w{0,50})/$',views.get_model_data),
]
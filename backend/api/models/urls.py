# basic URL Configurations
from django.urls import include, path, re_path
# import routers
from rest_framework import routers
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
    path('', views.index, name='index'),
    path('predModels/',views.task_list),
    re_path(r'update/(?P<stock_symbol>\w{0,50})/(?P<version>\w{0,50})/',views.update_model),
    re_path(r'get-pred/(?P<stock_symbol>\w{0,50})/',views.get_pred),
    re_path(r'train/(?P<stock_symbol>\w{0,50})/(?P<num_nodes>\w{0,50})/(?P<should_save>\w{0,5})/',views.admin_train),
    re_path(r'models/(?P<stock_symbol>\w{0,50})/get/all/',views.get_all_stock_model_versions_data),
    re_path(r'models/(?P<stock_symbol>\w{0,50})/',views.admin_models),
]
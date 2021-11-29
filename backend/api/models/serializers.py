# import serializer from rest_framework
from rest_framework import serializers
  
# import model from models.py
from .models import PredModel
  
# Create a model serializer 
class Serializer(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = PredModel
        fields = ('id' ,'title', 'description')
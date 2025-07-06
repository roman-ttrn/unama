from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.models import Products # we get models and Products from anothrer app wich stores this data
from products.serializers import ProductSerializer # Импортируется класс ProductSerializer из модуля products.serializers.

@api_view(['POST']) # allowed methods 
def api_home(req):
    serializer = ProductSerializer(data=req.data) # instance of serializer with appropriate data and make it dict
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save() # instance of model
        print(serializer.data)
        data = serializer.data
        return Response(serializer.data)
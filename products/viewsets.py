from rest_framework import viewsets

from .models import Products
from .serializers import ProductSerializer
from api.mixins import IsStaffEditorMixin

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default

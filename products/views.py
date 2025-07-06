from rest_framework import authentication, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404

from .models import Products
from .serializers import ProductSerializer
from api.authentication import TokenAuthentication
from api.mixins import (IsStaffEditorMixin, 
                        FilterUserProducts)

class ProductDetailAPIView(generics.RetrieveAPIView, 
                           IsStaffEditorMixin):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [ 
        authentication.SessionAuthentication,
        TokenAuthentication
    ]    
    

product_detail_view = ProductDetailAPIView.as_view()

class ProductListCreateAPIView(FilterUserProducts,
                               IsStaffEditorMixin,
                               generics.ListCreateAPIView): # create smth or if query has no particular pk it will output list of database data
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication,
    ]

    def perform_create(self, serializer):
        # email = serializer.validated_data.pop('email')
        print(type(Products.objects))
        content = serializer.validated_data.get('content')
        title = serializer.validated_data.get('title')  
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content) # form.save or mode.save()
        # send Django the signal

    #FILTER IS HERE!
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     # if we do not have IsStaffEditorMixin:
    #     #   if not self.request.user.is_authenticated:
    #     #        return Products.objects.none()
    #     return qs.filter(user=self.request.user)
product_list_create_view = ProductListCreateAPIView.as_view()


@api_view(["GET", "POST"])
def list_create_details(req, pk=None, *args, **kwargs):
    if req.method == "POST":
        serializer = ProductSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(req.data)

    if req.method == "GET":
        if pk:
            obj = get_object_or_404(Products, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        query_set = Products.objects.all()
        data = ProductSerializer(query_set, many=True).data 
        return Response(data)
    


class ProductListDeleteAPIView(generics.DestroyAPIView, IsStaffEditorMixin): 
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destr(self, instance):
        super().perform_destroy(instance)

delete_prod = ProductListDeleteAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView, IsStaffEditorMixin): 
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer): # serializer = ProductSerializer(data=req.data)
        instance = serializer.save() # grab instance of serializer where we can find certain rows
        if not instance.content:
            instance.content = instance.title

update = ProductUpdateAPIView.as_view()


# now here is the general class-bsaed view using mixin
# it contains all functions higher

class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
    IsStaffEditorMixin
):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, req, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(req, *args, **kwargs)
        return self.list(req, *args, **kwargs)
    
    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        print(request)
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

prduct_mixin = ProductMixinView.as_view()
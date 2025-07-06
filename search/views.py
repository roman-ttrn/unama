from rest_framework import generics
from django.shortcuts import render

from products.models import (Products)
from products.serializers import ProductSerializer

class SearchListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        res = Products.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            res = qs.search(q, user=user)
        return res

def algoliaSearch(req):
    return render(req, 'alg_search.html')
from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchListView.as_view(), name='search'),
    path("alg/", views.algoliaSearch, name="alg"),
]

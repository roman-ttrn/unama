from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list_create_view, name='products-list'),
    path('<int:pk>/', views.product_detail_view, name='product-detail'),
    path('<int:pk>/delete/', views.prduct_mixin, name='product-delete'),
    path('<int:pk>/update/', views.prduct_mixin, name='product-edit'),
]

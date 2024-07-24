from django.urls import path
from product.apps import ProductConfig
from product.views import product_list, product_detail

app_name = ProductConfig.name

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail')
]

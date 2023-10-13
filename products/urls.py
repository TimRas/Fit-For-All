from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('buy/<int:product_id>/', views.auth_check_buy_product,
         name='buy_product'),
    path('<int:product_id>/details', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_bag, name='show_bag'),
    path('add/<item_id>', views.add_to_bag, name='add_to_bag')
]
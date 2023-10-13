from django.urls import path
from . import views


urlpatterns = [
    path('plans_main', views.plans_main, name='plans_main'),
    path('plans_category/<str:category_title>/', views.show_plans_category, name='plans_category'),
    path('details/<int:challenge_id>/', views.view_challenge, name='challenges'),
    path('add/', views.add_challenge, name='add_challenge'),
]


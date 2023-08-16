from django.urls import path
from . import views


urlpatterns = [
    path('plans_main', views.plans_main, name='plans_main'),
    path('plans_category/<str:category_title>/', views.show_plans_category, name='plans_category'),
    path('<challenge_id>/details', views.view_challenge, name='challenges'),

]
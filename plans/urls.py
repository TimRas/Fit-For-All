from django.urls import path
from . import views


urlpatterns = [
    path('workout', views.workout_plans, name='workout_plans'),
    path('diet', views.diet_plans, name='diet_plans'),
]
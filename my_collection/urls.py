from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_collection, name='my_collection'),
    path('add/', views.add_shirt, name='add_shirt'),
]
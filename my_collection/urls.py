from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_collection, name='my_collection'),
    path('add/', views.add_shirt, name='add_shirt'),
    path('register/', views.register, name='register'),
    path('edit/<int:shirt_id>/', views.edit_shirt, name='edit_shirt'),
    path('delete/<int:shirt_id>/', views.delete_shirt, name='delete_shirt'),
]
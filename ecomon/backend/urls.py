"""
URL configuration for ecomon project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('example_view',views.example_view),
    path("", views.index),
]

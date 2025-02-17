"""
URL configuration for ecomon project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('example_view',views.example_view),
    path('home', views.home),
    path('packs', views.packs),
    path('scanner', views.scanner),
    path('profile', views.profile),
    path('',views.index)
]

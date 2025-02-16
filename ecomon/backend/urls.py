"""
URL configuration for ecomon project.
"""
from django.urls import path
from .views import render_scanner, render_gym_battle

urlpatterns = [
    path('scanner/', render_scanner, name='scanner'),
    path('gym-battle/<str:gym_id>/', render_gym_battle, name='gym-battle'),
]

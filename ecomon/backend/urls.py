"""
URL configuration for ecomon project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('scanner/', views.render_scanner, name='scanner'),
    path('gym-battle/<str:gym_id>/', views.render_gym_battle, name='gym-battle'),
]

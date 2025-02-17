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
    path('',views.index),
    path('scanner/', views.render_scanner, name='scanner'),
    path('gym-battle/<str:gym_id>/', views.render_gym_battle, name='gym-battle'),
]

"""
URL configuration for ecomon project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('packs', views.open_pack),
    path('opening_pack', views.opening_pack),
    path('scanner', views.scanner),
    path('profile', views.profile),
    path('',views.index),
    path('scanner/', views.render_scanner, name='scanner'),
    path('gym-battle/<str:gym_id>/', views.render_gym_battle, name='gym-battle'),
]

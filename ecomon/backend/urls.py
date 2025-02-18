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
    path('api/cards/', views.get_cards, name='get_cards'),
    path('api/player-cards/', views.get_player_cards,name='get_player_cards'),
]

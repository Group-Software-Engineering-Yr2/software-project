"""
URL configuration for ecomon project.
"""
from django.urls import path
from . import views
from .views import logout_view 


urlpatterns = [
    path('home', views.home),
    path('packs', views.open_pack),
    path('opening_pack', views.opening_pack),
    path('scanner', views.scanner),
    path('profile', views.profile),
    path('',views.index),
    path('scanner/', views.render_scanner, name='scanner'),
    path('gym-battle/<str:gym_id>/', views.render_gym_battle, name='gym-battle'),
    path('logout/', logout_view, name='logout'),
    path('change_deck', views.change_deck, name='change_deck'),
    path('update-deck/', views.update_deck, name='update_deck'),
]

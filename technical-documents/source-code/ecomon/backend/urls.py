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
    path('profile', views.profile),
    path('', views.index),
    path('scanner/', views.render_scanner, name='scanner'),
    path('view-gym/<str:gym_id>/', views.render_gym_view, name='view-gym'),
    path('gym-battle/<str:gym_id>/', views.render_gym_battle, name='gym-battle'),
    path('gym-battle-completed/', views.completed_gym_battle, name='gym-battle-completed'),
    path('gym-not-found/', views.gym_not_found, name='gym-not-found'),
    path('missing-battle-condition/', views.missing_battle_condition, name='missing-battle-condition'),
    path('battle-deck-empty/', views.user_has_no_deck, name='battle-deck-empty'),
    path('get_gym_locations/', views.get_gym_locations, name='get_gym_locations'),
    path('logout/', logout_view, name='logout'),
    path('change_deck', views.change_deck, name='change_deck'),
    path('update-deck/', views.update_deck, name='update_deck'),
]

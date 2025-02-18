'''Gym service module'''
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Card,Gym, PlayerCards

COOLDOWN_TIME_MINUTES = 30

def reset_profile_wrappers(user) -> None:
    '''
    Procedure to reset the wrapper count of a user
    '''
    profile = Profile.objects.get(user=user)
    profile.wrapper_count = 0
    profile.save()

def update_gym_cards(player_cards:list[PlayerCards],gym:Gym) -> None:
    '''
    Procedure to update the gym for the winner
    - Sets the cards for the gym
    - Updates the in_gym field of the PlayerCards
    '''
    cards = [card.card for card in player_cards]
    _set_gym_cards(cards,gym)
    _player_cards_in_use(player_cards)

def _player_cards_in_use(cards:list[PlayerCards])->None:
    '''
    Procedure to update the in_gym field of PlayerCards
    '''
    for card in cards:
        card.in_gym = True
        card.save()

def _set_gym_cards(cards:list[Card],gym:Gym) -> None:
    '''
    Procedure to set the cards for a gym
    '''
    for x,card in enumerate(cards):
        if x == 0:
            gym.card1 = card
        elif x == 1:
            gym.card2 = card
        elif x == 2:
            gym.card3 = card
    gym.save()

def update_owning_player(gym:Gym,user:User)->None:
    '''
    Procedure to update the owning player of a gym
    '''
    gym.owning_player = user
    gym.save()

def update_cooldown(gym:Gym)->None:
    '''
    Procedure to update the cooldown of a gym
    '''
    gym.cooldown = datetime.now() + timedelta(minutes=COOLDOWN_TIME_MINUTES)
    gym.save()

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Gym, PlayerCards

def reset_profile_wrappers(user:User):
    '''Resets the wrapper count for the user'''
    profile = Profile.objects.get(user=user)
    profile.wrapper_count = 0
    profile.save()

def update_gym_cards(user:User,cards,gym:Gym):
    '''Update cards in gym & holds player's cards'''
    _update_gym_cards(cards,gym)
    _update_player_cards(user,cards)

def _update_gym_cards(cards,gym:Gym):
    '''Updates the cards in the gym'''
    gym.card1 = cards[0]
    gym.card2 = cards[1]
    gym.card3 = cards[2]
    gym.save()

def _update_player_cards(user:User,cards):
    '''Updates the player's cards to be in use'''
    for card in cards:
        player_card = PlayerCards.objects.get(player=user,card=card)
        player_card.in_gym = True
        player_card.save()

def update_owning_player(user:User,gym:Gym):
    '''Updates the owning player of the gym'''
    gym.owning_player = user
    gym.save()


def update_cooldown(gym:Gym):
    '''Updates the cooldown of the gym'''
    gym.cooldown = timezone.now() + timedelta(minutes=30)
    gym.save()
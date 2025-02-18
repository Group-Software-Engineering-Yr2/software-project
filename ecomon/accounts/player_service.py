'''Player Service Module'''
from django.contrib.auth.models import User
from backend.models import PlayerCards
from .models import Profile


def get_player_deck(user:User) -> list[PlayerCards]:
    '''
    Function to get the player's deck
    '''
    profile = Profile.objects.get(user=user)

    return [profile.deck_card_1,profile.deck_card_2,profile.deck_card_3]

def has_deck(user:User) -> bool:
    '''
    Function to check if the player has a deck
    '''
    profile = Profile.objects.get(user=user)
    return profile.deck_card_1 is not None and profile.deck_card_2 is not None and profile.deck_card_3 is not None

def add_players_pack(user:User) -> None:
    '''
    Function to add a card to the player's pack
    '''
    profile = Profile.objects.get(user=user)
    profile.pack_count += 1
    profile.save()

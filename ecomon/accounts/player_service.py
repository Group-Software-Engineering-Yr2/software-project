from .models import Profile
from backend.models import Card

def get_player_deck(user) ->list[Card]:
    '''Returns the Cards of the player, not the PlayerCards'''
    profile = Profile.objects.get(user=user)
    cards = []
    cards.append(profile.deck_card_1)
    cards.append(profile.deck_card_2)
    cards.append(profile.deck_card_3)
    return cards

def has_deck(user):
    '''Check if the player has a deck'''
    profile = Profile.objects.get(user=user)
    if profile.deck_card_1 and profile.deck_card_2 and profile.deck_card_3:
        return True
    return False

def add_players_pack(user):
    '''Add a pack to the player's profile'''
    profile = Profile.objects.get(user=user)
    profile.pack_count += 1
    profile.save()
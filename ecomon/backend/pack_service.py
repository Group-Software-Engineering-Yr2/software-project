'''
Service for pack related operations
'''
import random
from accounts.models import Profile
from .models import Card, PlayerCards
from django.contrib.auth.models import User

PROBABILITIES = {
    1: 0.7,
    2: 0.2,
    3: 0.1
}


def get_pack_count(user) -> int:
    '''
    Based on the user, return the number of packs they have

    Returns the number of packs a user has
    '''
    profile = Profile.objects.get(user=user)
    return profile.pack_count

def generate_pack() -> list[Card]:
    '''
    Generate a pack for the user

    Returns a list of three packs
    '''
    # Plastic is 1
    # Recycle is 2
    # Plant is 3
    selected_cards = []

    for _ in range(3):
        # Choose a random type based on the probabilities
        chosen_type = random.choices(
            population=[1, 2, 3],
            weights=[PROBABILITIES[1], PROBABILITIES[2], PROBABILITIES[3]],
            k=1
        )[0]
        # Get a random card of that type
        card = Card.objects.filter(card_type=chosen_type).order_by('?').first()
        if card:
            selected_cards.append(card)

    return selected_cards

def reduce_user_pack_count(user) -> None:
    '''
    Removes a pack from the user's profile
    '''
    profile = Profile.objects.get(user=user)
    profile.pack_count -= 1
    profile.save()

def add_player_cards(user:User, cards:list[Card]) -> None:
    '''
    Adds the cards to the user's collection
    '''
    for card in cards:      
        if PlayerCards.objects.filter(player=user, card=card).exists():
            continue
        entry = PlayerCards.objects.create(
            player = user,
            card = card,
            in_gym = False,
            use_count = 0
        )
        entry.save()

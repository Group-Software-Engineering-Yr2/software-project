from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Gym, PlayerCards
from django.db import transaction

@transaction.atomic
def reset_profile_wrappers(user: User):
    '''Resets the wrapper count for the user'''
    #Nested transaction safety fixed bin not emptying bug - kept debug statements incase reoccurs
    with transaction.atomic():
        try:
            print(f"Resetting wrappers for user {user.username}")
            profile = Profile.objects.select_for_update().get(user=user)
            initial_count = profile.wrapper_count
            print(f"Initial wrapper count: {initial_count}")
            
            profile.wrapper_count = 0
            profile.save()
            
            # Force a refresh from database
            profile = Profile.objects.get(user=user)
            print(f"Final wrapper count: {profile.wrapper_count}")
            
            if profile.wrapper_count != 0:
                raise Exception(f"Failed to reset wrapper count. Still at {profile.wrapper_count}")
                
            return True
        except Exception as e:
            print(f"Error in reset_profile_wrappers: {str(e)}")
            raise

@transaction.atomic
def increase_bins_emptied(user: User):
    '''Increases the bins emptied count'''
    #Nested transaction safety fixed wrappers disposed - kept debug statements incase reoccurs
    with transaction.atomic():
        try:
            print(f"Increasing bins emptied for user {user.username}")
            profile = Profile.objects.select_for_update().get(user=user)
            initial_count = profile.bins_emptied
            print(f"Initial bins emptied: {initial_count}")
            
            profile.bins_emptied += 1
            profile.save()
            
            # Force a refresh from database
            profile = Profile.objects.get(user=user)
            print(f"Final bins emptied: {profile.bins_emptied}")
            
            if profile.bins_emptied <= initial_count:
                raise Exception(f"Failed to increase bins emptied. Before: {initial_count}, After: {profile.bins_emptied}")
                
            return True
        except Exception as e:
            print(f"Error in increase_bins_emptied: {str(e)}")
            raise

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

def increase_win_count(user:User):
    '''Increases the win count of the user'''
    profile = Profile.objects.get(user=user)
    profile.battles_won += 1
    profile.save()
    
def reset_gym_player_cards(gym:Gym):
    '''Resets the player's cards back to the user if the gym they were in is taken over by another player'''
    user = gym.owning_player
    cards_in_gym = [gym.card1,gym.card2,gym.card3]
    for card in cards_in_gym:
        # If the player's card has decomposed don't change the card that doesn't exists.
        try:
            player_card = PlayerCards.objects.get(player=user,card=card)
            player_card.in_gym = False
            player_card.save()
        except:
            pass
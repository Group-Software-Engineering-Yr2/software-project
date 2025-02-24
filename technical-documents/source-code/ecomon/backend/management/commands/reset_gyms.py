from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from backend.models import Gym, Card, PlayerCards
from accounts.models import User

class Command(BaseCommand):
    '''
    Cron Function to reset gyms including
    - Setting the cooldown to now
    - Updates the current owning player's cards to not in use
    - Setting the gym to team fossil fuel (arbitrary fossil fuel owner)
    - Randomising the cards within
    '''
    help = 'Resets the gyms to a default state'

    def handle(self, *args, **kwargs):

        def _get_gyms() -> list[Gym]:
            return Gym.objects.all()

        def _set_cooldown(gym: Gym):
            gym.cooldown = timezone.now()
            gym.save()

        def _set_team(gym: Gym):
            gym.owning_player = User.objects.get(username='fossil_fuel')
            gym.save()

        def _set_cards(gym: Gym):
            # Randomise the cards in gym
            cards = list(Card.objects.all().order_by('?')[:3])
            gym.card1 = cards[0]
            gym.card2 = cards[1]
            gym.card3 = cards[2]
            gym.save()

        def _update_owning_player_cards(gym: Gym):
            owning_player:User = gym.owning_player
            # Based on the three in the gym, please update this player's cards to not have them
            PlayerCards.objects.filter(player=owning_player, card=gym.card1).update(in_gym=False)
            PlayerCards.objects.filter(player=owning_player, card=gym.card2).update(in_gym=False)
            PlayerCards.objects.filter(player=owning_player, card=gym.card3).update(in_gym=False)

        print(f"Executing {datetime.now()}!")

        # Update all the gyms
        gyms = _get_gyms()
        for gym in gyms:
            # If team fossil fuel dont update their cards
            if gym.owning_player.username != 'fossil_fuel':
                _update_owning_player_cards(gym)
            _set_cooldown(gym)
            _set_team(gym)
            _set_cards(gym)

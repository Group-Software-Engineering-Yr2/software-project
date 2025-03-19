from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile, Team
from backend.models import Gym, Card, PlayerCards
from django.utils import timezone
from django.test import Client
import json

class TestBattles(TestCase):
    '''
    Test cases for battles
    '''
    def setUp(self):
        self.client = Client()
        # Use a dummy string instead of an image file.
        self.dummy_icon = "dummy/path.jpg"

        # Create teams.
        self.team_selectable = Team.objects.create(
            name="Recycle",
            color="green",
            icon=self.dummy_icon,
            user_selectable=True
        )
        self.team_selectable2 = Team.objects.create(
            name="Reuse",
            color="blue",
            icon=self.dummy_icon,
            user_selectable=True
        )
        self.team_nonselectable = Team.objects.create(
            name="NonSelectable",
            color="black",
            icon=self.dummy_icon,
            user_selectable=False
        )

        # Create dummy cards representing different types.
        self.card_plastic = Card.objects.create(
            name="Plastic Card",
            image=self.dummy_icon,
            card_type=1,
            ability_name_1="Plastic Ability 1",
            ability_power_1=1,
            ability_name_2="Plastic Ability 2",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Plastic fact"
        )
        self.card_recycle = Card.objects.create(
            name="Recycle Card",
            image=self.dummy_icon,
            card_type=2,
            ability_name_1="Recycle Ability 1",
            ability_power_1=1,
            ability_name_2="Recycle Ability 2",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Recycle fact"
        )
        self.card_plant = Card.objects.create(
            name="Plant Card",
            image=self.dummy_icon,
            card_type=3,
            ability_name_1="Plant Ability 1",
            ability_power_1=1,
            ability_name_2="Plant Ability 2",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Plant fact"
        )

        # Create a user and profile.
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword123"
        )
        self.profile = self.create_profile(self.user, self.team_selectable)

        # Create a gym for testing.
        self.gym = self.create_gym(
            owning_player=self.user,
            card1=self.card_plastic,
            card2=self.card_recycle,
            card3=self.card_plant,
            name="Test Gym",
            fact="Test fact",
            latitude=0.0,
            longitude=0.0
        )

    def create_profile(self, user, team):
        """
        Helper to create a Profile with required fields.
        """
        return Profile.objects.create(
            user=user,
            team_name=team,
            wrapper_count=0,
            pack_count=0,
            last_pack_allocation=timezone.now()
        )

    def create_gym(self, owning_player, card1, card2, card3, name="Test Gym", fact="Test fact",
                   latitude=0.0, longitude=0.0, cooldown=None):
        """
        Helper to create a Gym with all required fields.
        """
        if cooldown is None:
            cooldown = timezone.now()
        return Gym.objects.create(
            name=name,
            fact=fact,
            card1=card1,
            card2=card2,
            card3=card3,
            owning_player=owning_player,
            latitude=latitude,
            longitude=longitude,
            cooldown=cooldown
        )

    def test_view_gym_renders_correct_template_and_context(self):
        """
        Verify that a logged-in user gets a 200 response, the correct template is used,
        and that the context includes gym data (excluding gym cards) and the player's deck cards.
        """
        # Create a user assigned to team_selectable.
        user = User.objects.create_user(username='user1', password='pass')
        self.create_profile(user, self.team_selectable)
        self.client.login(username='user1', password='pass')

        # Create a gym for this user using a mix of card types.
        gym = self.create_gym(
            owning_player=user,
            card1=self.card_plastic,
            card2=self.card_recycle,
            card3=self.card_plant,
            name="Test Gym",
            fact="Test fact",
            latitude=0.0,
            longitude=0.0
        )

        # Add some cards to the player's deck.
        player_card1 = PlayerCards.objects.create(
            player=user,  # Use 'player' instead of 'user'
            card=self.card_plastic,
            in_gym=False,  # Use 'in_gym' instead of 'in_deck'
            use_count=0
        )
        player_card2 = PlayerCards.objects.create(
            player=user,  # Use 'player' instead of 'user'
            card=self.card_recycle,
            in_gym=False,  # Use 'in_gym' instead of 'in_deck'
            use_count=0
        )

        # Make a request to the view-gym page.
        response = self.client.get(f'/view-gym/{gym.id}/')

        # Verify the response status code and template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/battles/view_gym.html')

        # Verify the context contains the gym data (excluding gym cards).
        self.assertIn('gym_id', response.context)
        self.assertIn('gym_name', response.context)
        self.assertIn('gym_fact', response.context)
        self.assertIn('gym_latitude', response.context)
        self.assertIn('gym_longitude', response.context)
        self.assertIn('gym_cooldown', response.context)

        # Verify the gym data matches the created gym.
        self.assertEqual(response.context['gym_id'], str(gym.id))
        self.assertEqual(response.context['gym_name'], gym.name)
        self.assertEqual(response.context['gym_fact'], gym.fact)
        self.assertEqual(response.context['gym_latitude'], gym.latitude)
        self.assertEqual(response.context['gym_longitude'], gym.longitude)
        self.assertEqual(response.context['gym_cooldown'], gym.cooldown.timestamp())

        # Verify the context contains the player's deck cards.
        self.assertIn('player_deck_card1', response.context)
        self.assertIn('player_deck_card2', response.context)
        self.assertIn('player_deck_card3', response.context)

        # Verify the details of the player's deck cards.
        # Since the view passes individual cards, check if they match the cards added to the deck.
        self.assertEqual(response.context['player_deck_card1'], None)  # No card assigned
        self.assertEqual(response.context['player_deck_card2'], None)  # No card assigned
        self.assertEqual(response.context['player_deck_card3'], None)  # No card assigned

    def test_view_gym_redirect_if_not_logged_in(self):
        """
        The view is decorated with @login_required, so unauthenticated requests
        should be redirected to the login page.
        """
        response = self.client.get(f'/view-gym/{self.gym.id}/')  # Use the gym ID created in setUp
        self.assertRedirects(response, f'/accounts/login/?next=/view-gym/{self.gym.id}/', status_code=302)
    
    def test_gym_battle_renders_correct_template_and_context(self):
        """
        Verify that a logged-in user gets a 200 response, the correct template is used,
        and that the context includes the player's deck cards, gym cards, and other required data.
        """
        # Create a user assigned to team_selectable.
        user = User.objects.create_user(username='user1', password='pass')
        self.create_profile(user, self.team_selectable)
        self.client.login(username='user1', password='pass')

        # Create a gym for this user using a mix of card types.
        gym = self.create_gym(
            owning_player=user,
            card1=self.card_plastic,
            card2=self.card_recycle,
            card3=self.card_plant,
            name="Test Gym",
            fact="Test fact",
            latitude=0.0,
            longitude=0.0
        )

        # Add some cards to the player's deck.
        player_card1 = PlayerCards.objects.create(
            player=user,
            card=self.card_plastic,
            in_gym=False,
            use_count=0
        )
        player_card2 = PlayerCards.objects.create(
            player=user,
            card=self.card_recycle,
            in_gym=False,
            use_count=0
        )
        player_card3 = PlayerCards.objects.create(
            player=user,
            card=self.card_plant,
            in_gym=False,
            use_count=0
        )

        # Assign the player's deck cards.
        user.profile.deck_card_1 = Card.objects.get(name="Plastic Card")
        user.profile.deck_card_2 = Card.objects.get(name="Recycle Card")
        user.profile.deck_card_3 = Card.objects.get(name="Plant Card")
        user.profile.save()

        # Make a request to the gym_battle page.
        response = self.client.get(f'/gym-battle/{gym.id}/')

        # Verify the response status code and template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/battles/gym_battle.html')

        # Verify the context contains the player's deck cards.
        self.assertIn('player_deck_card1', response.context)
        self.assertIn('player_deck_card2', response.context)
        self.assertIn('player_deck_card3', response.context)

        player_deck_card1_data = json.loads(response.context['player_deck_card1'])
        player_deck_card2_data = json.loads(response.context['player_deck_card2'])
        player_deck_card3_data = json.loads(response.context['player_deck_card3'])

        # Verify the player's deck cards match the cards added to the deck.
        self.assertEqual(player_deck_card1_data['name'], self.card_plastic.name)
        self.assertEqual(player_deck_card2_data['name'], self.card_recycle.name)
        self.assertEqual(player_deck_card3_data['name'], self.card_plant.name)

        # Verify the context contains the gym's cards.
        self.assertIn('gym_card1', response.context)
        self.assertIn('gym_card2', response.context)
        self.assertIn('gym_card3', response.context)

        gym_card1_data = json.loads(response.context['gym_card1'])
        gym_card2_data = json.loads(response.context['gym_card2'])
        gym_card3_data = json.loads(response.context['gym_card3'])

        # Verify the gym's cards match the cards assigned to the gym.
        self.assertEqual(gym_card1_data['name'], self.card_plastic.name)
        self.assertEqual(gym_card2_data['name'], self.card_recycle.name)
        self.assertEqual(gym_card3_data['name'], self.card_plant.name)

        # Verify other context variables.
        self.assertIn('username', response.context)
        self.assertIn('user_team', response.context)
        self.assertIn('gym_owning_player', response.context)
        self.assertIn('gym_team', response.context)
        self.assertIn('gym_id', response.context)

        # Verify the values of other context variables.
        self.assertEqual(response.context['username'], user.username)
        self.assertEqual(response.context['user_team'], self.team_selectable.name)
        self.assertEqual(response.context['gym_owning_player'].username, gym.owning_player.username)
        self.assertEqual(response.context['gym_team'], self.team_selectable.name)
        self.assertEqual(response.context['gym_id'], str(gym.id))


    def test_gym_battle_redirect_if_not_logged_in(self):
        """
        The gym battle view is protected by @login_required.
        Unauthenticated requests should be redirected.
        """
        response = self.client.get(f'/gym-battle/{self.gym.id}/')
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/gym-battle/{self.gym.id}/')
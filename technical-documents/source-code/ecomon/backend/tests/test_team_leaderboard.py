from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from backend.models import Gym, Card, Team
from accounts.models import Profile

class TeamLeaderboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Use a dummy string instead of a image file.
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

    def test_redirect_if_not_logged_in(self):
        """
        The team leaderboard view is protected by @login_required.
        Unauthenticated requests should be redirected.
        """
        response = self.client.get('/team_leaderboard')
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=' + '/team_leaderboard')

    def test_renders_correct_template_and_context(self):
        """
        Verify that a logged-in user gets a 200 response, the correct template is used,
        and that the context includes team data with correct aggregation.
        """
        # Create a user assigned to team_selectable.
        user = User.objects.create_user(username='user1', password='pass')
        self.create_profile(user, self.team_selectable)
        self.client.login(username='user1', password='pass')

        # Create one gym for this user using a mix of card types.
        self.create_gym(user, self.card_plastic, self.card_recycle, self.card_plant)
        response = self.client.get('/team_leaderboard')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/leaderboard/team_leaderboard.html')
        self.assertIn('teams', response.context)
        teams_data = response.context['teams']

        # Only teams marked as user_selectable should appear.
        team_data = next(
            (team for team in teams_data if team['name'] == self.team_selectable.name),
            None
        )
        self.assertIsNotNone(team_data)
        # We created 1 gym for a user in team_selectable, currently_owned_gyms should be 1.
        self.assertEqual(team_data['currently_owned_gyms'], 1)
        # For that gym, the card types should be counted:
        self.assertEqual(team_data['plastic_cards_in_use'], 1)
        self.assertEqual(team_data['recycle_cards_in_use'], 1)
        self.assertEqual(team_data['plant_cards_in_use'], 1)
        # Check that the dummy icon link is used.
        self.assertEqual(team_data['icon_url'],'/'+ self.dummy_icon)

    def test_multiple_gyms_and_cards(self):
        """
        Test a team with multiple gyms and various card combinations.
        """
        user = User.objects.create_user(username='user2', password='pass')
        self.create_profile(user, self.team_selectable)
        self.client.login(username='user2', password='pass')

        # Create three gyms with distinct card combinations.
        self.create_gym(user, self.card_plastic, self.card_plastic, self.card_plastic)
        self.create_gym(user, self.card_recycle, self.card_recycle, self.card_recycle)
        self.create_gym(user, self.card_plant, self.card_plant, self.card_plant)

        response = self.client.get('/team_leaderboard')
        teams_data = response.context['teams']
        team_data = next(
            (team for team in teams_data if team['name'] == self.team_selectable.name),
            None
        )
        self.assertIsNotNone(team_data)
        # Expect 3 gyms.
        self.assertEqual(team_data['currently_owned_gyms'], 3)
        # Gym 1 contributes 3 plastic cards. Gym 2 contributes 3 recycle cards. Gym 3 contributes 3 plant cards.
        self.assertEqual(team_data['plastic_cards_in_use'], 3)
        self.assertEqual(team_data['recycle_cards_in_use'], 3)
        self.assertEqual(team_data['plant_cards_in_use'], 3)

    def test_team_with_no_gyms(self):
        """
        Verify that a team with no gyms owned by its users still appears in the context with zero counts.
        """
        # Create a user for team_selectable2 but no gyms.
        user = User.objects.create_user(username='user3', password='pass')
        self.create_profile(user, self.team_selectable2)
        self.client.login(username='user3', password='pass')

        response = self.client.get('/team_leaderboard')
        teams_data = response.context['teams']
        team_data = next(
            (team for team in teams_data if team['name'] == self.team_selectable2.name),
            None
        )
        self.assertIsNotNone(team_data)
        self.assertEqual(team_data['currently_owned_gyms'], 0)
        self.assertEqual(team_data['plastic_cards_in_use'], 0)
        self.assertEqual(team_data['recycle_cards_in_use'], 0)
        self.assertEqual(team_data['plant_cards_in_use'], 0)

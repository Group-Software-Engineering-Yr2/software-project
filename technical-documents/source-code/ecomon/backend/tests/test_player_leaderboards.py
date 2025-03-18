from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from backend.models import Gym, PlayerCards, Card, Team
from accounts.models import Profile

class PlayerLeaderboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create teams for testing.
        self.team_good = Team.objects.create(
            name="Recycle",
            color="green",
            icon="dummy/path.jpg",
            user_selectable=True
        )
        self.team_bad = Team.objects.create(
            name="Fossil Fuels",
            color="red",
            icon="dummy/path.jpg",
            user_selectable=True
        )
        # Create a dummy card to use in Gym instances.
        self.dummy_card = Card.objects.create(
            name="Test Card",
            image="dummy/path.jpg",
            card_type=1,
            ability_name_1="Test Ability 1",
            ability_power_1=1,
            ability_name_2="Test Ability 2",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Test fact"
        )

    def create_profile(self, user, team, battles_won=0, bins_emptied=0, packs_opened=0,
                       wrapper_count=0, pack_count=0):
        """
        Helper method to create a Profile with required stats.
        """
        return Profile.objects.create(
            user=user,
            team_name=team,
            battles_won=battles_won,
            bins_emptied=bins_emptied,
            packs_opened=packs_opened,
            wrapper_count=wrapper_count,
            pack_count=pack_count,
            last_pack_allocation=timezone.now()
        )
    
    def create_gym(self, owning_player, name="Test Gym", fact="Test fact",
                   latitude=0.0, longitude=0.0, cooldown=None):
        """
        Helper method to create a Gym with all required fields.
        """
        if cooldown is None:
            cooldown = timezone.now()
        return Gym.objects.create(
            name=name,
            fact=fact,
            card1=self.dummy_card,
            card2=self.dummy_card,
            card3=self.dummy_card,
            owning_player=owning_player,
            latitude=latitude,
            longitude=longitude,
            cooldown=cooldown
        )
    
    def test_redirect_if_not_logged_in(self):
        """
        The view is decorated with @login_required, so unauthenticated requests
        should be redirected to the login page.
        """
        # Ensure that the urls.py includes a URL pattern with name 'player_leaderboard'
        response = self.client.get('/player_leaderboard')
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=' + '/player_leaderboard')

    def test_renders_correct_template_and_context(self):
        """
        Ensure that a logged-in user gets a 200 response,
        the correct template is used, and the context contains the expected keys.
        """
        user = User.objects.create_user(username='user1', password='pass')
        self.create_profile(user, self.team_good, battles_won=10, bins_emptied=5, packs_opened=2)
        # Create a few gyms for this user.
        for _ in range(3):
            self.create_gym(user)

        self.client.login(username='user1', password='pass')
        response = self.client.get('/player_leaderboard')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/leaderboard/player_leaderboard.html')
        self.assertIn('players', response.context)
        players = response.context['players']
        self.assertEqual(len(players), 1)

        player_data = players[0]
        self.assertEqual(player_data['username'], 'user1')
        self.assertEqual(player_data['team_name'], self.team_good.name)
        self.assertEqual(player_data['owning_gyms'], 3)
        self.assertEqual(player_data['battles_won'], 10)
        self.assertEqual(player_data['bins_emptied'], 5)
        self.assertEqual(player_data['packs_opened'], 2)

    def test_excludes_fossil_fuels_team(self):
        """
        Players whose team is "Fossil Fuels" should be excluded from the leaderboard.
        """
        good_user = User.objects.create_user(username='good_user', password='pass')
        bad_user = User.objects.create_user(username='bad_user', password='pass')

        self.create_profile(good_user, self.team_good, battles_won=5, bins_emptied=3, packs_opened=1)
        self.create_profile(bad_user, self.team_bad, battles_won=20, bins_emptied=10, packs_opened=4)

        self.client.login(username='good_user', password='pass')
        response = self.client.get('/player_leaderboard')
        players = response.context['players']
        usernames = [player['username'] for player in players]
        self.assertIn('good_user', usernames)
        self.assertNotIn('bad_user', usernames)

    def test_ordering_by_owning_gyms(self):
        """
        The leaderboard should be sorted in descending order by the number of gyms owned.
        """
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        user3 = User.objects.create_user(username='user3', password='pass')

        self.create_profile(user1, self.team_good)
        self.create_profile(user2, self.team_good)
        self.create_profile(user3, self.team_good)

        # Assign gyms: user1 gets 2 gyms, user2 gets 5 gyms, user3 gets 1 gym.
        for _ in range(2):
            self.create_gym(user1)
        for _ in range(5):
            self.create_gym(user2)
        for _ in range(1):
            self.create_gym(user3)

        self.client.login(username='user1', password='pass')
        response = self.client.get('/player_leaderboard')
        players = response.context['players']

        # Expected order: user2 (5 gyms), then user1 (2 gyms), then user3 (1 gym).
        self.assertEqual(players[0]['username'], 'user2')
        self.assertEqual(players[1]['username'], 'user1')
        self.assertEqual(players[2]['username'], 'user3')

    def test_player_cards_count(self):
        """
        Verify that the counts of player cards (by type) and the collection total are computed correctly.
        """
        user = User.objects.create_user(username='card_user', password='pass')
        self.create_profile(user, self.team_good, battles_won=15, bins_emptied=7, packs_opened=3)
        # Create a gym for this user.
        self.create_gym(user)

        # Create card instances.
        card_plastic = Card.objects.create(
            name="Plastic Card",
            image="dummy/path.jpg",
            card_type=1,
            ability_name_1="Plastify",
            ability_power_1=1,
            ability_name_2="Compress",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Plastic fact"
        )
        card_recycle = Card.objects.create(
            name="Recycle Card",
            image="dummy/path.jpg",
            card_type=2,
            ability_name_1="Recycle",
            ability_power_1=1,
            ability_name_2="Reprocess",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Recycle fact"
        )
        card_plant = Card.objects.create(
            name="Plant Card",
            image="dummy/path.jpg",
            card_type=3,
            ability_name_1="Grow",
            ability_power_1=1,
            ability_name_2="Bloom",
            ability_power_2=1,
            ability_self_power_2=0,
            health_points=1,
            fact="Plant fact"
        )

        # Create PlayerCards: 1 plastic cards, 1 recycle card, 1 plant card.
        PlayerCards.objects.create(player=user, card=card_plastic, in_gym=False, use_count=0)
        PlayerCards.objects.create(player=user, card=card_recycle, in_gym=False, use_count=0)
        PlayerCards.objects.create(player=user, card=card_plant, in_gym=False, use_count=0)

        self.client.login(username='card_user', password='pass')
        response = self.client.get('/player_leaderboard')
        players = response.context['players']
        self.assertEqual(len(players), 1)
        player_data = players[0]
        self.assertEqual(player_data['plastic_cards_owned'], 1)
        self.assertEqual(player_data['recycle_cards_owned'], 1)
        self.assertEqual(player_data['plant_cards_owned'], 1)
        self.assertEqual(player_data['collection_total'], 3)

    def test_limit_top_10_players(self):
        """
        If more than 10 players exist, the leaderboard should include only the top 10 (ordered by gym count).
        """
        # Create 15 users with an increasing number of gyms.
        for i in range(15):
            user = User.objects.create_user(username=f'user{i}', password='pass')
            self.create_profile(user, self.team_good)
            # Each user gets i gyms.
            for _ in range(i):
                self.create_gym(user)

        self.client.login(username='user0', password='pass')
        response = self.client.get('/player_leaderboard')
        players = response.context['players']

        # There should be no more than 10 players in the context.
        self.assertEqual(len(players), 10)
        # The first player should have the highest gym count (i.e. user14 with 14 gyms).
        self.assertEqual(players[0]['owning_gyms'], 14)

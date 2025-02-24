from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Profile, Team
from backend.models import Gym,Card,PlayerCards

class AuthenticatedNonAuthenticatedUserAccessTest(APITestCase):
    '''Test cases for authenticated user access'''
    def setUp(self):
        """Set up a test user and team"""
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        #Create cards
        self.card1 = Card.objects.create(
            name="TestCard1",
            image="TestImage1",
            card_type=1,
            ability_name_1="TestAbilityName1",
            ability_power_1=1,
            ability_name_2="TestAbilityName2",
            ability_power_2=2,
            health_points=100,
            fact="TestFact1"
        )
        self.card2 = Card.objects.create(
            name="TestCard2",
            image="TestImage2",
            card_type=2,
            ability_name_1="TestAbilityName1",
            ability_power_1=1,
            ability_name_2="TestAbilityName2",
            ability_power_2=2,
            health_points=100,
            fact="TestFact2"
        )
        self.card3 = Card.objects.create(
            name="TestCard3",
            image="TestImage3",
            card_type=3,
            ability_name_1="TestAbilityName1",
            ability_power_1=1,
            ability_name_2="TestAbilityName2",
            ability_power_2=2,
            health_points=100,
            fact="TestFact3"
        )

        # Create player cards
        self.player_card1 = PlayerCards.objects.create(
            card=self.card1,
            player=self.user,
            in_gym=False,
            use_count=0
        )
        self.player_card2 = PlayerCards.objects.create(
            card=self.card2,
            player=self.user,
            in_gym=False,
            use_count=0
        )
        self.player_card3 = PlayerCards.objects.create(
            card=self.card3,
            player=self.user,
            in_gym=False,
            use_count=0
        )
        # Create a gym
        self.gym = Gym.objects.create(
            id=1,
            name="TestGym",
            fact="some fact",
            owning_player=self.user,
            latitude=0,
            longitude=0,
            cooldown=timezone.now(),
            card1=self.card1,
            card2=self.card2,
            card3=self.card3,
        )
        # Create profile
        self.profile = Profile.objects.create(
            user=self.user, team_name=self.team, wrapper_count=0, pack_count=1, 
            deck_card_1=self.card1, deck_card_2=self.card2, deck_card_3=self.card3
        )

    
    # Testing pack page access
    def test_authenticated_user_redirect(self):
        """Test authenticated user is redirected to home page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/packs")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_redirect(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/packs", follow=True)  # Follow redirects
        self.assertRedirects(response, "/accounts/login/?next=/packs", status_code=302, target_status_code=200)

    # Home page access
    def test_authenticated_user_home_page(self):
        """Test authenticated user can access home page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/home")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_home_page(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/home", follow=True)  # Follow redirects
        self.assertRedirects(response, "/accounts/login/?next=/home", status_code=302, target_status_code=200)

    # Profile page access
    def test_authenticated_user_profile_page(self):
        """Test authenticated user can access profile page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/profile")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_profile_page(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/profile", follow=True)
        self.assertRedirects(response, "/accounts/login/?next=/profile", status_code=302, target_status_code=200)

    # Scanner page access
    def test_authenticated_user_scanner_page(self):
        """Test authenticated user can access scanner page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/scanner/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_scanner_page(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/scanner/", follow=True)
        self.assertRedirects(response, "/accounts/login/?next=/scanner/", status_code=302, target_status_code=200)

    # Gym battle page access
    def test_authenticated_user_gym_battle_page(self):
        """Test authenticated user can access gym battle page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/gym-battle/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_gym_battle_page(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/gym-battle/1/", follow=True)
        self.assertRedirects(response, "/accounts/login/?next=/gym-battle/1/", status_code=302, target_status_code=200)
    
    # Gym battle completed page access
    def test_authenticated_user_gym_battle_completed_page(self):
        """Test authenticated user can access gym battle completed page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(f"/gym-battle-completed/?did_win=true&gym_id={self.gym.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_gym_battle_completed_page(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/gym-battle-completed?did_win=true&gym_id={self.gym.id}", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Change deck page access
    def test_authenticated_user_change_deck_page(self):
        """Test authenticated user can access change deck page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/change_deck")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_change_deck_page(self):
        """Test unauthenticated user is redirected to login page"""
        response = self.client.get("/change_deck", follow=True)
        self.assertRedirects(response, "/accounts/login/?next=/change_deck", status_code=302, target_status_code=200)
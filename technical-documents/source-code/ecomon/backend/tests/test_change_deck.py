from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Team, Profile
from backend.models import Card, PlayerCards

class DeckViewsTests(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test user and login
        self.client = Client()
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            team_name=self.team,
            wrapper_count=0,
            pack_count=0,
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
        
        # Add cards to player's collection
        PlayerCards.objects.create(
            player=self.user,
            card=self.card1,
            in_gym=False,
            use_count=0
        )
        PlayerCards.objects.create(
            player=self.user,
            card=self.card2,
            in_gym=False,
            use_count=0
        )
        PlayerCards.objects.create(
            player=self.user,
            card=self.card3,
            in_gym=False,
            use_count=0
        )
        
        # Login the test user
        self.client.login(username='testuser', password='testpass123')

    def test_change_deck_view(self):
        """Test the change deck view"""
        # Test GET request
        response = self.client.get(reverse('change_deck'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/profile/changeDeck.html')
        
        # Check context
        self.assertIn('cards', response.context)
        self.assertIn('player_cards', response.context)
        self.assertIn('deck_card_1', response.context)
        self.assertIn('deck_card_2', response.context)
        self.assertIn('deck_card_3', response.context)
        
        # Check referrer handling
        response = self.client.get(
            reverse('change_deck'),
            HTTP_REFERER='/profile/'
        )
        self.assertEqual(
            self.client.session.get('original_referrer'),
            '/profile/'
        )

    def test_update_deck_view(self):
        """Test the update deck view"""
        # Test POST request with valid data matching the form structure
        post_data = {
            'selected_cards': [  
                self.card1.name,
                self.card2.name, 
                self.card3.name
            ],
            'card_order': [  # Add this to match what the view expects
                self.card1.name,
                self.card2.name,
                self.card3.name
            ]
        }
        
        # Set original referrer in session
        session = self.client.session
        session['original_referrer'] = reverse('change_deck')
        session.save()
        
        # Make the POST request
        response = self.client.post(
            reverse('update_deck'),
            data=post_data,
            follow=True
        )
        
        # Check redirect
        self.assertRedirects(
            response,
            reverse('change_deck'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        
        # Refresh profile from db
        self.profile.refresh_from_db()
        
        # Check if deck was updated
        self.assertEqual(self.profile.deck_card_1.name, self.card1.name)
        self.assertEqual(self.profile.deck_card_2.name, self.card2.name)
        self.assertEqual(self.profile.deck_card_3.name, self.card3.name)

        
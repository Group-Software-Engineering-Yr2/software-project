from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Team, Profile
from backend.models import Achievement, PlayerAchievements
from backend.achievement_service import check_and_award_achievements

class AchievementServiceTests(TestCase):
    
    def setUp(self):
        """Set up a test user and team"""
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )

         # Create profile for the user
        self.profile = Profile.objects.create(
            user=self.user,
            team_name=self.team,
            wrapper_count=0,
            pack_count=0
        )

          # Create test achievements
        Achievement.objects.create(
            name='Bronze Pack Opener',
            type='PACKS',
            threshold=10,
            tier=1
        )
        Achievement.objects.create(
            name='Silver Battler ',
            type='BATTLES',
            threshold=25,
            tier=2
        )
        Achievement.objects.create(
            name='Gold Binner',
            type='BINS',
            threshold=50,
            tier=3
        )




    def test_pack_achievement(self):
        """Test pack opening achievement"""
        # Set initial packs opened
        self.user.profile.packs_opened = 10
        self.user.profile.save()
        
        # Get initial pack count
        initial_packs = self.user.profile.pack_count
        
        # Check achievements
        awarded = check_and_award_achievements(self.user, 'PACKS')
        
        # Verify results
        self.assertTrue(awarded)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.pack_count, initial_packs + 1)
        self.assertTrue(
            PlayerAchievements.objects.filter(
                player=self.user,
                achievement__name='Bronze Pack Opener'
            ).exists()
        )

    def test_pack_reward(self):
        """Test pack reward for new achievement"""
        # Set initial packs opened 
        self.user.profile.packs_opened = 10
        self.user.profile.save()

        # Get initial pack count
        initial_packs = self.user.profile.pack_count
        
        # Check achievements
        awarded = check_and_award_achievements(self.user, 'PACKS')
        
        # Verify results
        self.assertTrue(awarded)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.pack_count, initial_packs + 1)

    def test_pack_rewards_not_doubled(self):
        """Test pack rewards are not given twice for the same achivement"""
        # Set initial packs opened
        self.user.profile.packs_opened = 10
        self.user.profile.save()
        
        # Get initial pack count
        initial_packs = self.user.profile.pack_count
        
        # Check achievements
        awarded = check_and_award_achievements(self.user, 'PACKS')
        
        # Verify results
        self.assertTrue(awarded)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.pack_count, initial_packs + 1)
        
        # Check achievements again
        awarded = check_and_award_achievements(self.user, 'PACKS')
        
        # Verify results
        self.assertFalse(awarded)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.pack_count, initial_packs + 1)

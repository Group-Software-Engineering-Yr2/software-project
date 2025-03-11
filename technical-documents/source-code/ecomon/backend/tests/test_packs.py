
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile, Team
from backend.models import Gym,Card,PlayerCards


class TestPacks(TestCase):
    '''
    Test cases for packs
    '''
    def setUp(self):
        '''Set up the database for the test'''
        self.team =  Team.objects.create(name='test',color='test',icon='test',user_selectable=True)
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            team_name=self.team,
            deck_card_1=None,
            deck_card_2=None,
            deck_card_3=None,
            wrapper_count=0,
            pack_count=1,
            last_pack_allocation="2025-03-03"
        )

    def test_open_pack_correct_settings(self):
        '''Test open pack page with a pack and no wrappers'''
        # Ensure correct values
        self.profile.wrapper_count = 0
        self.profile.pack_count = 1
        self.profile.save()
        # Login
        self.client.login(username='testuser', password='testpassword123')
        # Test
        response = self.client.get('/opening_pack')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/packs/opening_pack.html')

    def test_open_pack_no_pack(self):
        '''Test open pack page with no packs'''
        # Ensure correct values
        self.profile.wrapper_count = 0
        self.profile.pack_count = 0
        self.profile.save()
        # Login
        self.client.login(username='testuser', password='testpassword123')
        # Test
        response = self.client.get('/opening_pack')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/packs', status_code=302, target_status_code=200)
        # Seperate response to check if the packs page is rendered
        response2 = self.client.get('/packs')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'backend/packs/nopacks.html')


    def test_open_pack_full_bin(self):
        '''Test open pack page with a full bin & pack available'''
        # Ensure correct values
        self.profile.wrapper_count = 10
        self.profile.pack_count = 1
        self.profile.save()
        # Login
        self.client.login(username='testuser', password='testpassword123')
        # Test
        response = self.client.get('/opening_pack')
        self.assertEqual(response.status_code, 302) # redirects to
        self.assertRedirects(response, '/packs', status_code=302, target_status_code=200)
        # Seperate response to check if the packs page is rendered
        response2 = self.client.get('/packs')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'backend/packs/bin_full.html')

    def test_open_pack_no_pack_bin(self):
        '''Test open pack page with no pack & no wrappers'''
        # Ensure correct values
        self.profile.wrapper_count = 0
        self.profile.pack_count = 0
        self.profile.save()
        # Login
        self.client.login(username='testuser', password='testpassword123')
        # Test
        response = self.client.get('/opening_pack')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/packs', status_code=302, target_status_code=200)
        # Seperate response to check if the packs page is rendered
        response2 = self.client.get('/packs')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'backend/packs/nopacks.html')
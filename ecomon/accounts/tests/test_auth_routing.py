from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Profile, Team

class AuthenticatedUserAccessTests(APITestCase):
    '''Test cases for authenticated user access'''
    def setUp(self):
        """Set up a test user and team"""
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.profile = Profile.objects.create(
            user=self.user, team_name=self.team, wrapper_count=0, pack_count=1
        )

    def test_authenticated_user_redirect(self):
        """Test authenticated user is redirected to home page"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/home")

    def test_unauthenticated_user_redirect(self):
        """Test unauthenticated user is redirected to signup page"""
        response = self.client.get("/", follow=True)  # Follow redirects
        self.assertRedirects(response, "/accounts/register/", status_code=302, target_status_code=200)

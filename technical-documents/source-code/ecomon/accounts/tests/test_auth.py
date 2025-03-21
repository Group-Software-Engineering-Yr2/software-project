from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import Profile, Team


class APIAuthenticationTests(APITestCase):
    '''Test cases for API user authentication'''
    def setUp(self):
        """Set up a test user and team"""
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        # Auth token used for api auth
        self.token = Token.objects.create(user=self.user) 
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.profile = Profile.objects.create(
            user=self.user, team_name=self.team, wrapper_count=0, pack_count=2
        )

    def tearDown(self):
        """Clean up database changes after each test"""
        self.client.credentials() 
        Profile.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Token.objects.all().delete()

    def test_register_user(self):
        """Test user registration"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "team_name": "TestTeam"
        }
        response = self.client.post("/accounts/api/register/", data, format="json")
        print("Register Response:", response.data)  # Debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_gets_one_pack_on_registration(self):
        """Test that new users receive one pack on registration"""

        data = {
            "username": "packuser",  # Changed username to avoid conflict
            "email": "packuser@example.com",
            "password": "testpassword123",
            "team_name": "TestTeam"  # Match the team name from setUp
        }

        # Make POST request to register endpoint using correct path
        response = self.client.post("/accounts/api/register/", data, format="json")
        
        # Check if registration was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the created user and verify pack count
        new_user = User.objects.get(username="packuser")
        profile = Profile.objects.get(user=new_user)
        self.assertEqual(profile.pack_count, 2)


    def test_login_user(self):
        """Test user login"""
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post("/accounts/api/login/", data, format="json")
        print("Login Response:", response.data)  # Debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_get_profile(self):
        """Test fetching user profile"""
        response = self.client.get("/accounts/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "testuser")

    def test_update_profile(self):
        """Test updating profile information"""
        data = {"wrapper_count": 10, "pack_count": 7}
        response = self.client.put("/accounts/api/profile/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.wrapper_count, 10)
        self.assertEqual(self.profile.pack_count, 7)

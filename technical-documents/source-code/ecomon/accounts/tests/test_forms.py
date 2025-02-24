from django.test import TestCase
from accounts.forms import CustomUserCreationForm
from accounts.models import Team

class TestForms(TestCase):
    '''
    Test cases for forms
    '''
    def setUp(self):
        self.team = Team.objects.create(name="TestTeam")

    def tearDown(self):
        """Clean up database changes after each test"""
        Team.objects.all().delete()

    def test_custom_user_creation_form(self):
        """Test form validation for user creation"""
        form_data = {
            "username": "formuser",
            "email": "formuser@example.com",
            "password1": "securepassword",
            "password2": "securepassword",
            "team": self.team.pk
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

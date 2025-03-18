from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile, Team
from django.utils import timezone

class TestScanner(TestCase):
    '''
    Test cases for scanner
    '''
    def setUp(self):
        '''Set up the database for the test'''
        self.team =  Team.objects.create(name='test',color='test',icon='test',user_selectable=True)
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword123"
        )

        self.dummy_icon = "dummy/path.jpg"
        self.team_selectable = Team.objects.create(
            name="Recycle",
            color="green",
            icon=self.dummy_icon,
            user_selectable=True
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
    
    def test_scan_renders_correct_template(self):
        """
        Verify that a logged-in user gets a 200 response, the correct template is used
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/scanner/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/scanner/scanner.html')

    def test_scan_redirect_if_not_logged_in(self):
        """
        The view is decorated with @login_required, so unauthenticated requests
        should be redirected to the login page.
        """
        response = self.client.get('/scanner/')  # Ensure trailing slash
        self.assertRedirects(response, '/accounts/login/?next=/scanner/', status_code=302)
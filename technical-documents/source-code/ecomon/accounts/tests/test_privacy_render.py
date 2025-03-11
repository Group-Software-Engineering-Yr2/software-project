from django.test import TestCase
from accounts.forms import CustomUserCreationForm

class TestForms(TestCase):
    '''
    Test cases for the privacy page
    '''

    def test_privacy_page_renders(self):
        '''Test that the privacy page renders successfully'''
        response = self.client.get('/accounts/privacy/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/privacy.html')
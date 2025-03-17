from django.test import TestCase

class TestPrivacy(TestCase):
    '''
    Test cases for the privacy page
    '''

    def test_privacy_page_renders(self):
        '''Test that the privacy page renders successfully'''
        response = self.client.get('/accounts/privacy/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/privacy.html')

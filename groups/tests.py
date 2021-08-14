from django.test import TestCase


class TestPage(TestCase):
    '''Test for http status code = 200 OK '''

    def test_group_landing_page_works(self):
        response = self.client.get('/groups/')
        self.assertEqual(response.status_code, 200)

    

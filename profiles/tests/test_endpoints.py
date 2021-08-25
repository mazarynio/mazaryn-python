from django.urls import reverse
from rest_framework.test import APITestCase
from profiles import models

class TestEndpoints(APITestCase):
    
    def test_mobile_login_works(self):
        user = models.User.objects.create_user("user1", "abcabcabc")
        response = self.client.post(reverse("mobile_token"),
                                    {"username": "user1", "password": "abcabcabc"},
                                    )
        jsonresp = response.json()
        self.assertIn("token", jsonresp)
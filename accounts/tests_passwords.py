from django.test import TestCase
from django.contrib.auth.models import User

class PasswordResetTests(TestCase):
    def test_password_reset_view(self):
        User.objects.create_user('u1', email='u1@example.com', password='p')
        resp = self.client.get('/accounts/password_reset/')
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.post('/accounts/password_reset/', data={'email': 'u1@example.com'})
        # should redirect to done
        self.assertEqual(resp2.status_code, 302)

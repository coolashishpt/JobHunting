from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class AccountsTests(TestCase):
    def test_signup_creates_profile(self):
        resp = self.client.post('/accounts/signup/', data={'username': 'alice', 'email': 'a@example.com', 'password1': 'passw0rd123', 'password2': 'passw0rd123', 'role': 'candidate'})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='alice')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_login_logout(self):
        User.objects.create_user('bob', password='secret')
        login = self.client.post('/accounts/login/', data={'username': 'bob', 'password': 'secret'})
        self.assertEqual(login.status_code, 302)
        resp = self.client.get('/accounts/logout/')
        self.assertEqual(resp.status_code, 302)

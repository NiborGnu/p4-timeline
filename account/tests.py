from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


class AccountViewsTests(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password
            )


def test_login_user_get(self):
    response = self.client.get(self.login_url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/login.html')


def test_login_user_post_success(self):
    response = self.client.post(
        self.login_url,
        {'username': self.username, 'password': self.password},
        follow=True)
    self.assertRedirects(response, reverse('home'))
    self.assertContains(response, 'You have successfully logged in')


def test_login_user_post_failure(self):
    response = self.client.post(
        self.login_url,
        {'username': self.username, 'password': 'wrongpassword'},
        follow=True)
    self.assertContains(response, 'Error logging in. Please try again')

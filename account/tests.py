from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


class AccountViewsTests(TestCase):
    def setUp(self):
        """
        Set up test data for account views.
        Creates a test user and defines URL for login.
        """
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_login_user_get(self):
        """
        Test GET request for login page.
        Checks if the page loads successfully and uses the correct template.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_user_post_success(self):
        """
        Test POST request for successful login.
        Checks if login redirects to the home page and
        displays a success message.
        """
        response = self.client.post(
            self.login_url,
            {'username': self.username, 'password': self.password},
            follow=True  # Follow redirects
        )
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'You have successfully logged in')

    def test_login_user_post_failure(self):
        """
        Test POST request for failed login.
        Checks if login attempt with wrong password shows an error message.
        """
        response = self.client.post(
            self.login_url,
            {'username': self.username, 'password': 'wrongpassword'},
            follow=True  # Follow redirects
        )
        self.assertContains(response, 'Error logging in. Please try again')

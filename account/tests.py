from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


class AccountViewsTests(TestCase):
    def setUp(self):
        # Define the URL for the login page
        self.login_url = reverse('login')

        # Define test user credentials
        self.username = 'testuser'
        self.password = 'securepassword'

        # Create a test user with the specified credentials
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    # Test the GET request for the login page
    def test_login_user_get(self):
        response = self.client.get(self.login_url)
        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'account/login.html')

    # Test the POST request for a successful login
    def test_login_user_post_success(self):
        response = self.client.post(
            self.login_url,
            {'username': self.username, 'password': self.password},
            follow=True  # Follow redirects
        )
        # Check if the response redirects to the home page
        self.assertRedirects(response, reverse('home'))
        # Check if the success message is present in the response
        self.assertContains(response, 'You have successfully logged in')

    # Test the POST request for a failed login
    def test_login_user_post_failure(self):
        response = self.client.post(
            self.login_url,
            {'username': self.username, 'password': 'wrongpassword'},
            follow=True  # Follow redirects
        )
        # Check if the error message is present in the response
        self.assertContains(response, 'Error logging in. Please try again')

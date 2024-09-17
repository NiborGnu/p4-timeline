from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import TimePost
from user.models import Profile


class HomeViewsTests(TestCase):

    def setUp(self):
        # URLs for home and search pages
        self.home_url = reverse('home')
        self.search_url = reverse('search')

        # Test user credentials
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        # Create a profile for the test user
        Profile.objects.get_or_create(user=self.user)

        # Log in the test user
        self.client.login(
            username=self.username,
            password=self.password
        )

    def test_homepage_get(self):
        # Test if the homepage loads successfully
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_create_timepost_success(self):
        # Test if a TimePost is created successfully
        response = self.client.post(
            self.home_url,
            {'body': 'This is a test TimePost'}
        )
        # Expect a redirect to the home page
        self.assertRedirects(response, self.home_url)
        # Check if the TimePost is in the database
        self.assertTrue(
            TimePost.objects.filter(body='This is a test TimePost').exists()
        )

    def test_search_functionality(self):
        # Create another user for search functionality test
        other_user = User.objects.create_user(
            username='otheruser',
            password='password'
        )
        Profile.objects.get_or_create(user=other_user)
        # Perform search for the new user
        response = self.client.get(
            self.search_url,
            {'q': 'otheruser'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'otheruser')

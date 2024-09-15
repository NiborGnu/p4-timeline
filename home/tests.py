from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import TimePost
from user.models import Profile


class HomeViewsTests(TestCase):

    def setUp(self):
        self.home_url = reverse('home')
        self.search_url = reverse('search')
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        # Ensure Profile is created only if it does not already exist
        Profile.objects.get_or_create(user=self.user)

        self.client.login(
            username=self.username,
            password=self.password
        )

    def test_homepage_get(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_create_timepost_success(self):
        response = self.client.post(
            self.home_url,
            {'body': 'This is a test TimePost'}
        )
        # Expect a redirect to the home page or an appropriate URL
        self.assertRedirects(response, self.home_url)
        # Verify TimePost is created
        self.assertTrue(
            TimePost.objects.filter(body='This is a test TimePost').exists()
        )

    def test_search_functionality(self):
        # Create another profile to search for
        other_user = User.objects.create_user(
            username='otheruser',
            password='password'
        )
        Profile.objects.get_or_create(user=other_user)
        response = self.client.get(
            self.search_url,
            {'q': 'otheruser'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'otheruser')

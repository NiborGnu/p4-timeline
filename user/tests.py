from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Profile
from home.models import TimePost


class ProfileTests(TestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1', password='password'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password'
        )
        self.user3 = User.objects.create_user(
            username='user3', password='password'
        )

        # Create profiles
        self.profile1 = Profile.objects.get_or_create(user=self.user1)[0]
        self.profile2 = Profile.objects.get_or_create(user=self.user2)[0]
        self.profile3 = Profile.objects.get_or_create(user=self.user3)[0]

        # Create timeposts
        self.timepost1 = TimePost.objects.create(
            user=self.user1, body='Post by user1'
        )
        self.timepost2 = TimePost.objects.create(
            user=self.user2, body='Post by user2'
        )

        # Follow relationships
        self.profile1.follow.add(self.profile2)  # user1 follows user2
        self.profile2.follow.add(self.profile3)  # user2 follows user3

        # Create client instance and login
        self.client = Client()
        self.client.login(username='user1', password='password')

    def test_view_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)
        self.assertNotContains(response, self.user1.username)

    def test_view_profile(self):
        response = self.client.get(
            reverse('profile', args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.timepost1.body)

    def test_view_follows(self):
        response = self.client.get(
            reverse('follows', args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)
        self.assertNotContains(response, self.user3.username)

    def test_follow_unfollow(self):
        # Test following
        response = self.client.post(
            reverse('profile', args=[self.user2.id]),
            {'follow': 'follow'}
        )
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.assertRedirects(response, reverse(
            'profile', args=[self.user2.id]
            ))
        self.profile1.refresh_from_db()
        self.assertIn(self.profile2, self.profile1.follow.all())

        # Test unfollowing
        response = self.client.post(
            reverse('profile', args=[self.user2.id]),
            {'follow': 'unfollow'}
        )
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.assertRedirects(response, reverse(
            'profile', args=[self.user2.id]
            ))
        self.profile1.refresh_from_db()
        self.assertNotIn(self.profile2, self.profile1.follow.all())

    def test_delete_profile(self):
        # Ensure profile deletion works
        response = self.client.post(
            reverse('delete_profile', args=[self.user1.id])
        )
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(username='user1').exists())

    def test_no_profiles(self):
        # Simulate no profiles available
        Profile.objects.all().delete()
        response = self.client.get(reverse('users'))
        self.assertContains(
            response, "No profiles found"
        )  # Ensure this message appears when no profiles exist

    def tearDown(self):
        # Clean up after tests
        User.objects.all().delete()
        Profile.objects.all().delete()
        TimePost.objects.all().delete()

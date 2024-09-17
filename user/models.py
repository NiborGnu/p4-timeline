from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# User Profile model
class Profile(models.Model):
    """
    User Profile model that extends the
    built-in User model with additional features.

    Attributes:
        user: One-to-One relationship with the User model.
        follow: Many-to-Many relationship to allow users to follow other users.
        date_modified: Automatically updated timestamp
        for when the profile was last modified.
        bio: A text field for storing a biography or description.
    """
    # Link each Profile to a single User using a One-to-One relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    # A Profile can follow multiple other Profiles
    follow = models.ManyToManyField(
        'self',  # Self-referential relationship
        related_name='followed_by',  # Reverse relation for followers
        # Ensures it's a one-way follow (not auto-follow back)
        symmetrical=False,
        blank=True  # Allows the follow field to be empty initially
    )

    # Automatically updated timestamp for when the profile was last modified
    date_modified = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True, null=True)

    # Return the username when the Profile is represented as a string
    def __str__(self):

        return self.user.username


# Signal to create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a Profile instance whenever a new User is created.

    Args:
        sender: The model class that sent the signal.
        instance: The actual instance of the model.
        created: Boolean indicating if a new record was created.
        kwargs: Additional keyword arguments.
    """
    # Check if the User was just created
    if created:
        Profile.objects.get_or_create(user=instance)
        # Check if the Profile already exists
        if not hasattr(instance, 'profile'):
            # Create a Profile associated with the new User
            user_profile = Profile(user=instance)
            user_profile.save()

            # Set the User to follow themselves automatically
            user_profile.follow.set([user_profile.id])
            user_profile.save()

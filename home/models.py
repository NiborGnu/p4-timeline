from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# User Profile model
class Profile(models.Model):
    # Link each Profile to a single User using a One-to-One relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # A Profile can follow multiple other Profiles
    follow = models.ManyToManyField(
        'self',  # Self-referential relationship
        related_name='followed_by',  # Reverse relation for followers
        symmetrical=False,  # Ensures it's a one-way follow (not auto-follow back)
        blank=True  # Allows the follow field to be empty initially
    )
    
    # Automatically updated timestamp for when the profile was last modified
    date_modified = models.DateTimeField(auto_now=True)

    # Return the username when the Profile is represented as a string
    def __str__(self):
        return self.user.username

# Signal to create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Check if the User was just created
    if created:
        # Create a Profile associated with the new User
        user_profile = Profile(user=instance)
        user_profile.save()

        # Set the User to follow themselves automatically
        user_profile.follow.set([user_profile.id])
        user_profile.save()


# Create TimePost model
class TimePost(models.Model):
    # Link the TimePost to the user who created it
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # Body of the TimePost, limited to 400 characters
    body = models.CharField(max_length=400)
    # Timestamp for when the TimePost was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Many-to-Many field for users who liked the TimePost
    likes = models.ManyToManyField(
        User, 
        related_name='liked_posts',  # Reverse relation for the User's liked posts
        blank=True  # Allows the likes field to be empty initially
    )
    # Many-to-Many field for users who disliked the TimePost
    dislikes = models.ManyToManyField(
        User, 
        related_name='disliked_posts',  # Reverse relation for the User's disliked posts
        blank=True  # Allows the dislikes field to be empty initially
    )

    # Returns the total number of likes for the TimePost
    def number_of_likes(self):
        return self.likes.count()

    # Returns the total number of dislikes for the TimePost
    def number_of_dislikes(self):
        return self.dislikes.count()

    # TODO: Add an image to a post (Install Pillow!)
    # image = models.ImageField(upload_to='images/', blank=True, null=True)

    # TODO: Add a comment section to the post

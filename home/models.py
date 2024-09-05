from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# User Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField('self',
        related_name='followed_by',
        symmetrical=False,
        blank=True
    )
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# Create Profile when User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # User follows themself
        user_profile.follow.set([instance.profile.id])
        user_profile.save()


# Create TimePost model
class TimePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    # Like/Dislike to a post
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    
    # Number of likes
    def number_of_likes(self):
        return self.likes.count()
    
    # Number of dislikes
    def number_of_dislikes(self):
        return self.dislikes.count()
    
    # TODO: Add a image to a post (Install pillow!)
    # image = models.ImageField(upload_to='images/', blank=True, null=True)
    # TODO: Add a comment to a post

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


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


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timepost = models.ForeignKey(TimePost, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create TimePost model
class TimePost(models.Model):
    # Link the TimePost to the user who created it
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Body of the TimePost, limited to 400 characters
    body = models.CharField(max_length=400)
    # Timestamp for when the TimePost was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Many-to-Many field for users who liked the TimePost
    likes = models.ManyToManyField(
        User,
        # Reverse relation for the User's liked posts
        related_name='liked_posts',
        # Allows the likes field to be empty initially
        blank=True
    )
    # Many-to-Many field for users who disliked the TimePost
    dislikes = models.ManyToManyField(
        User,
        # Reverse relation for the User's disliked posts
        related_name='disliked_posts',
        # Allows the dislikes field to be empty initially
        blank=True
    )

    # Returns the total number of likes for the TimePost
    def number_of_likes(self):
        return self.likes.count()

    # Returns the total number of dislikes for the TimePost
    def number_of_dislikes(self):
        return self.dislikes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timepost = models.ForeignKey(
        TimePost, related_name='comments', on_delete=models.CASCADE
        )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

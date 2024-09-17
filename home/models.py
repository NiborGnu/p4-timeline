from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class TimePost(models.Model):
    """
    Model to represent a user's time post with likes and dislikes.
    """
    # Link the TimePost to the user who created it
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Body of the TimePost, limited to 400 characters
    body = models.CharField(max_length=400)

    # Timestamp for when the TimePost was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Many-to-Many field for users who liked the TimePost
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    # Many-to-Many field for users who disliked the TimePost
    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_posts',
        blank=True
    )

    def number_of_likes(self):
        """
        Return the total number of likes for the TimePost.
        """
        return self.likes.count()

    def number_of_dislikes(self):
        """
        Return the total number of dislikes for the TimePost.
        """
        return self.dislikes.count()


class Comment(models.Model):
    """
    Model to represent a comment on a TimePost.
    """
    # Foreign key linking to the User model.
    # If the user is deleted, cascade the deletion to comments.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Foreign key linking to the TimePost model.
    # 'comments' allows reverse access from TimePost to its comments.
    timepost = models.ForeignKey(
        TimePost, related_name='comments', on_delete=models.CASCADE
    )

    # Field to store the text content of the comment
    body = models.TextField()

    # Timestamp for when the comment was created, set automatically
    created_at = models.DateTimeField(auto_now_add=True)

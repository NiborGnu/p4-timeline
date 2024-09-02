from django.db import models
from django.contrib.auth.models import User

# User Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField('self',
        related_name='followed_by',
        symmetrical=False,
        blank=True)
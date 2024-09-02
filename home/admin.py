from django.contrib import admin
from django.contrib.auth.models import Group, User


# Unregister the default User, Group
admin.site.unregister(Group)
admin.site.unregister(User)


# User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Display username
    fields = ['username']


# Register the new User model
admin.site.register(User, UserAdmin)
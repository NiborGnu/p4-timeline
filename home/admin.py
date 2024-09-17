from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import TimePost
from user.models import Profile


# Unregister the default Group model from the admin interface
admin.site.unregister(Group)


class ProfileInline(admin.StackedInline):
    """
    Inline admin interface for the Profile model.
    """
    model = Profile


class UserAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the User model.
    """
    model = User
    # Display only the username field
    fields = ['username']
    inlines = [ProfileInline]


# Unregister the default User model from the admin interface
admin.site.unregister(User)


# Register the User model with the custom UserAdmin interface
admin.site.register(User, UserAdmin)


# Register the TimePost model in the admin interface
admin.site.register(TimePost)

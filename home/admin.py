from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import TimePost
from user.models import Profile


# Unregister the default Group
admin.site.unregister(Group)

# Put Profile in User Model
class ProfileInline(admin.StackedInline):
    model = Profile

# User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Display username
    fields = ['username']
    inlines = [ProfileInline]

# Unregister the default User
admin.site.unregister(User)

# Register the new User
admin.site.register(User, UserAdmin)

# Register TimePost
admin.site.register(TimePost)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from home.models import TimePost
from user.models import Profile

@login_required
def users(request):
    # Get all users excluding the current user's profile
    users = Profile.objects.exclude(user=request.user)
    # Render the users page with the list of users
    return render(request, 'user/users.html', {'users': users})

@login_required
def profile(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    timeposts = TimePost.objects.filter(user_id=pk).order_by('-created_at')
    
    if request.method == 'POST':
        # Get current user profile
        current_user_profile = request.user.profile
        # Get form data
        action = request.POST.get('follow')
        
        if action == 'unfollow':
            current_user_profile.follow.remove(profile)
            messages.success(request, f'You have unfollowed {profile.user.username}')
        else:
            current_user_profile.follow.add(profile)
            messages.success(request, f'You are now following {profile.user.username}')
        # Redirect after processing the follow/unfollow action
        return redirect('profile', pk=pk)
    
    return render(request, 'user/profile.html', {'profile': profile, 'timeposts': timeposts})

@login_required
def followers(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    followers_list = profile.followed_by.exclude(user_id=request.user.id)
    
    if request.user.id == pk:
        return render(request, 'user/followers.html', {'followers': followers_list})
    else:
        messages.error(request, 'That is not your followers page')
        return redirect('home')

@login_required
def follows(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    follows_list = profile.follow.exclude(user_id=request.user.id)
    
    if request.user.id == pk:
        return render(request, 'user/follows.html', {'follows': follows_list})
    else:
        messages.error(request, 'That is not your follows page')
        return redirect('home')

@login_required
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if request.user != profile.user and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        # Delete all timeposts by the user
        timeposts = TimePost.objects.filter(user=profile.user)
        for timepost in timeposts:
            # Remove likes and dislikes
            timepost.likes.clear()
            timepost.dislikes.clear()
            # Delete all comments related to this timepost
            timepost.comments.all().delete()
            # Finally delete the timepost
            timepost.delete()


        # If the deleted profile was the current logged-in user, log them out
        if profile.user == request.user:
            # Delete the profile
            profile.user.delete()
            logout(request)
            messages.success(request, 'Your profile has been deleted successfully.')
            return redirect('home')  # Redirect to home or another page after deletion
        else:
            # If the profile being deleted belongs to someone else (handled by a superuser)
            profile.user.delete()  # Delete the user (profile will cascade delete if set up properly)
            messages.success(request, f'The profile for {profile.user.username} has been deleted successfully.')
            return redirect('users')  # Redirect to the users page after deletion

    # If not a POST request, just redirect to a confirmation page or home
    return redirect('home')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home.models import TimePost
from user.models import Profile


def users(request):
    if request.user.is_authenticated:
        # Get all users excluding the current user's profile
        users = Profile.objects.exclude(user=request.user)
        # Render the users page with the list of users
        return render(request, 'user/users.html', {'users': users})
    else:
        # Show a message if the user is not authenticated
        messages.success(request, 'You must be logged in to view this page')
        # Redirect to the home page
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        timeposts = TimePost.objects.filter(user_id=pk).order_by('-created_at')
        # Form logic
        if request.method == 'POST':
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Unfollow
            if action == 'unfollow':
                current_user_profile.follow.remove(profile)
            # Follow
            else:
                current_user_profile.follow.add(profile)
        return render(request, 'user/profile.html', {'profile': profile, 'timeposts': timeposts})
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')


def followers(request, pk):
    if request.user.is_authenticated:
        # Getting the right profile for the user ID (pk)
        profile = get_object_or_404(Profile, user_id=pk)
        # Get the followers of the user, excluding the current user's own profile
        followers_list = profile.followed_by.exclude(user_id=request.user.id)
        # Only allow the logged-in user to view their own followers page
        if request.user.id == pk:
            return render(request, 'user/followers.html', {'followers': followers_list})
        else:
            messages.success(request, 'That is not your followers page')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to view this page')
        return redirect('home')


def follows(request, pk):
    if request.user.is_authenticated:
        # Getting the right profile for the user ID (pk)
        profile = get_object_or_404(Profile, user_id=pk)
        # Get the profiles this user is following, excluding their own profile
        follows_list = profile.follow.exclude(user_id=request.user.id)
        # Only allow the logged-in user to view their own follows page
        if request.user.id == pk:
            return render(request, 'user/follows.html', {'follows': follows_list})
        else:
            messages.success(request, 'That is not your follows page')
            return redirect('home')
    else: 
        messages.success(request, 'You must be logged in to view this page')
        return redirect('home')
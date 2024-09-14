from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

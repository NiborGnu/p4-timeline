from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, TimePost


def index(request):
    if request.user.is_authenticated:
        timeposts = TimePost.objects.all().order_by('-created_at')

    return render(request, 'home/index.html', {'timeposts': timeposts})


def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'home/profiles.html', {'profiles': profiles})
    else: 
        messages.success(request, 'You must be logged in to view this page')
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




        return render(request, 'home/profile.html', {'profile': profile, 'timeposts': timeposts})
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')
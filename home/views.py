from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, TimePost
from .forms import TimePostForm


def index(request):
    if request.user.is_authenticated:
        form = TimePostForm(request.POST or None)
        if form.is_valid():
            timepost = form.save(commit=False)
            timepost.user = request.user
            timepost.save()
            messages.success(request, 'Your TimePost was created successfully')
            return redirect('home')


        timeposts = TimePost.objects.all().order_by('-created_at')
        return render(request, 'home/index.html', {'timeposts': timeposts, 'form': form})
    else:
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

def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow
        request.user.profile.follow.remove(profile)
        request.user.profile.save()
        # Message unfollowed(profile)
        messages.success(request, f'You have unfollowed {profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to Follow
        profile = Profile.objects.get(user_id=pk)
        # Follow
        request.user.profile.follow.add(profile)
        request.user.profile.save()
        # Message Followed(profile)
        messages.success(request, f'You are now following {profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')

def TimePost_like(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.likes.filter(id=request.user.id).exists():
        timepost.likes.remove(request.user)
    else:
        if timepost.dislikes.filter(id=request.user.id).exists():
            timepost.dislikes.remove(request.user)
        timepost.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

def TimePost_dislike(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.dislikes.filter(id=request.user.id).exists():
        timepost.dislikes.remove(request.user)
    else:
        if timepost.likes.filter(id=request.user.id).exists():
            timepost.likes.remove(request.user)
        timepost.dislikes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
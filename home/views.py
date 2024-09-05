from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, TimePost
from .forms import TimePostForm


def index(request):
    if request.user.is_authenticated:
        # Handle the form for creating a TimePost
        form = TimePostForm(request.POST or None)
        # If form is valid, save the TimePost
        if form.is_valid():
            timepost = form.save(commit=False)
            timepost.user = request.user
            timepost.save()
            messages.success(request, 'Your TimePost was created successfully')
            # Redirect to the home page after saving
            return redirect('home')
        # Get all TimePosts, ordered by creation date
        timeposts = TimePost.objects.all().order_by('-created_at')
        # Render the index page with TimePosts and the form
        return render(request, 'home/index.html', {'timeposts': timeposts, 'form': form})
    else:
        # Get all TimePosts if the user is not authenticated
        timeposts = TimePost.objects.all().order_by('-created_at')
        # Render the index page without the form for non-authenticated users
        return render(request, 'home/index.html', {'timeposts': timeposts})



def profiles(request):
    if request.user.is_authenticated:
        # Get all profiles excluding the current user's profile
        profiles = Profile.objects.exclude(user=request.user)
        # Render the profiles page with the list of profiles
        return render(request, 'home/profiles.html', {'profiles': profiles})
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
        return render(request, 'home/profile.html', {'profile': profile, 'timeposts': timeposts})
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')

def followers(request, pk):
    if request.user.is_authenticated:
        # Getting the right profile for the user ID (pk)
        profile = get_object_or_404(Profile, user_id=pk)
        # Get the followers of the user
        followers_list = profile.followed_by.all()
        # Only allow the logged-in user to view their own followers page
        if request.user.id == pk:
            return render(request, 'home/followers.html', {'followers': followers_list})
        else:
            messages.success(request, 'That is not your followers page')
            return redirect('home')
    else: 
        messages.success(request, 'You must be logged in to view this page')
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
    # Get the TimePost by its primary key (id)
    timepost = get_object_or_404(TimePost, id=pk)
    # Check if the current user has already liked the TimePost
    if timepost.likes.filter(id=request.user.id).exists():
        # If already liked, remove the like
        timepost.likes.remove(request.user)
    else:
        # If the user has disliked the post, remove the dislike first
        if timepost.dislikes.filter(id=request.user.id).exists():
            timepost.dislikes.remove(request.user)
        # Add the like to the TimePost
        timepost.likes.add(request.user)
    
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER'))

def TimePost_dislike(request, pk):
    # Get the TimePost by its primary key (id)
    timepost = get_object_or_404(TimePost, id=pk)
    # Check if the current user has already disliked the TimePost
    if timepost.dislikes.filter(id=request.user.id).exists():
        # If already disliked, remove the dislike
        timepost.dislikes.remove(request.user)
    else:
        # If the user has liked the post, remove the like first
        if timepost.likes.filter(id=request.user.id).exists():
            timepost.likes.remove(request.user)
        # Add the dislike to the TimePost
        timepost.dislikes.add(request.user)
    
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER'))
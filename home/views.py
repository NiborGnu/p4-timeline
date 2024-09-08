from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home.models import TimePost
from user.models import Profile
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


def timepost_like(request, pk):
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


def timepost_dislike(request, pk):
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


def delete_timepost(request, pk):
    if request.user.is_authenticated:
        timepost = get_object_or_404(TimePost, id=pk)
        if timepost.user == request.user:
            timepost.delete()
            messages.success(request, 'Your TimePost was deleted successfully')
        else:
            messages.error(request, "You don't have permission to delete this post.")
    else:
        messages.error(request, 'You must be logged in to remove TimePosts...')
        return redirect('home')
    return redirect(request.META.get('HTTP_REFERER'))


def edit_timepost(request, pk):
    if request.user.is_authenticated:
        timepost = get_object_or_404(TimePost, id=pk)
        if timepost.user == request.user:
            form = TimePostForm(request.POST or None, instance=timepost)
            if request.method == 'POST':
                if form.is_valid():
                    timepost = form.save(commit=False)
                    timepost.user = request.user
                    form.save()
                    messages.success(request, 'Your TimePost was updated successfully.')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'There was an error updating the TimePost.')
        else:
            form = TimePostForm(instance=timepost)
    else:
        messages.error(request, 'You must be logged in to edit TimePosts...')
        return redirect('home')
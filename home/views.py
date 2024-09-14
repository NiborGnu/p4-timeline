from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import TimePost, Comment
from user.models import Profile
from .forms import TimePostForm, CommentForm

def index(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Create a form instance, handling both GET and POST requests
        form = TimePostForm(request.POST or None)
        
        # Process the form when it is submitted (POST request)
        if request.method == 'POST' and form.is_valid():
            # Save the TimePost, associating it with the current user
            timepost = form.save(commit=False)
            timepost.user = request.user
            timepost.save()
            
            # Display a success message and redirect to home page
            messages.success(request, 'Your TimePost was created successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        
        # Retrieve all TimePosts, ordered by creation date (most recent first)
        timeposts = TimePost.objects.all().order_by('-created_at')
        
        # Render the index page with TimePosts and the form
        return render(request, 'home/index.html', {
            'timeposts': timeposts,
            'form': form
        })
    
    else:
        # For non-authenticated users, do not include the form
        timeposts = TimePost.objects.all().order_by('-created_at')
        
        # Render the index page with only TimePosts
        return render(request, 'home/index.html', {
            'timeposts': timeposts
        })


@login_required
def unfollow(request, pk):
    # Ensure user is authenticated
    profile = get_object_or_404(Profile, user_id=pk)
    # Unfollow the profile
    request.user.profile.follow.remove(profile)
    request.user.profile.save()
    messages.success(request, f'You have unfollowed {profile.user.username}')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def follow(request, pk):
    # Ensure user is authenticated
    profile = get_object_or_404(Profile, user_id=pk)
    # Follow the profile
    request.user.profile.follow.add(profile)
    request.user.profile.save()
    messages.success(request, f'You are now following {profile.user.username}')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def timepost_like(request, pk):
    # Get the TimePost by its primary key (id)
    timepost = get_object_or_404(TimePost, id=pk)
    # Check if the current user has already liked the TimePost
    if timepost.likes.filter(id=request.user.id).exists():
        timepost.likes.remove(request.user)  # If already liked, remove the like
    else:
        if timepost.dislikes.filter(id=request.user.id).exists():
            timepost.dislikes.remove(request.user)  # Remove dislike if it exists
        timepost.likes.add(request.user)  # Add the like
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def timepost_dislike(request, pk):
    # Get the TimePost by its primary key (id)
    timepost = get_object_or_404(TimePost, id=pk)
    # Check if the current user has already disliked the TimePost
    if timepost.dislikes.filter(id=request.user.id).exists():
        timepost.dislikes.remove(request.user)  # If already disliked, remove the dislike
    else:
        if timepost.likes.filter(id=request.user.id).exists():
            timepost.likes.remove(request.user)  # Remove like if it exists
        timepost.dislikes.add(request.user)  # Add the dislike
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_timepost(request, pk):
    # Ensure the user is authenticated
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.user == request.user:
        timepost.delete()
        messages.success(request, 'Your TimePost was deleted successfully')
    else:
        messages.error(request, "You don't have permission to delete this post.")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_timepost(request, pk):
    # Ensure the user is authenticated
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.user == request.user or request.user.is_superuser:
        form = TimePostForm(request.POST or None, instance=timepost)
        if request.method == 'POST':
            if form.is_valid():
                timepost = form.save(commit=False)
                timepost.user = request.user
                timepost.save()
                messages.success(request, 'The TimePost was updated successfully.')
                return redirect(request.META.get('HTTP_REFERER'))
        return render(request, 'home/edit_timepost.html', {
            'form': form, 
            'timepost': timepost
            })
    else:
        messages.error(request, 'You do not have permission to edit this TimePost.')
        return redirect('home')

def search(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        query = request.GET.get('q', '')
        if query:
            # Get all users that match the search
            results = Profile.objects.filter(user__username__icontains=query)
        else:
            results = Profile.objects.none()
        return render(request, 'home/search.html', {
            'results': results,
            'user': request.user,  # Pass the actual user object to the template
            'query': query  # Pass the query string if you need it in the template
        })
    else:
        # Redirect to login if the user is not authenticated
        return redirect('login')

@login_required
def add_comment(request, pk):
    # Ensure the user is authenticated
    timepost = get_object_or_404(TimePost, id=pk)
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            Comment.objects.create(user=request.user, timepost=timepost, body=comment_body)
            messages.success(request, 'Your comment was posted successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')
    # Update comment count for the specific TimePost
    comment_count = Comment.objects.filter(timepost=timepost).count()
    return redirect(f"{request.META.get('HTTP_REFERER')}?comment_count={comment_count}")

@login_required
def delete_comment(request, comment_id):
    # Ensure the user is authenticated
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_comment(request, comment_id):
    # Ensure the user is authenticated
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Comment edited successfully.')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'home/edit_comment.html', {
            'form': form, 
            'comment': comment
            })
    else:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('home')

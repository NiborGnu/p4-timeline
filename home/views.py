from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from home.models import TimePost, Comment
from user.models import Profile
from .forms import TimePostForm, CommentForm


def index(request):
    if request.user.is_authenticated:
        form = TimePostForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            timepost = form.save(commit=False)
            timepost.user = request.user
            timepost.save()
            messages.success(request, 'Your TimePost was created successfully')
            return redirect(request.GET.get('next', 'home'))

        timeposts = TimePost.objects.all().order_by('-created_at')
        return render(request, 'home/index.html', {
            'timeposts': timeposts,
            'form': form
        })
    else:
        timeposts = TimePost.objects.all().order_by('-created_at')
        return render(request, 'home/index.html', {
            'timeposts': timeposts
        })


@login_required
def follow(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    request.user.profile.follow.add(profile)
    request.user.profile.save()
    messages.success(request, f'You are now following {profile.user.username}')
    return redirect(request.POST.get('next', 'home'))

@login_required
def unfollow(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    request.user.profile.follow.remove(profile)
    request.user.profile.save()
    messages.success(request, f'You have unfollowed {profile.user.username}')
    return redirect(request.POST.get('next', 'home'))

@login_required
def timepost_like(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    
    # Toggle the like status
    if timepost.likes.filter(id=request.user.id).exists():
        timepost.likes.remove(request.user)
    else:
        # Remove the dislike if the user had previously disliked
        if timepost.dislikes.filter(id=request.user.id).exists():
            timepost.dislikes.remove(request.user)
        timepost.likes.add(request.user)
    
    # Redirect to the 'next' URL, or default to 'home' if not provided
    next_url = request.GET.get('next', 'home')
    return redirect(next_url)

@login_required
def timepost_dislike(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    
    # Toggle the dislike status
    if timepost.dislikes.filter(id=request.user.id).exists():
        timepost.dislikes.remove(request.user)
    else:
        # Remove the like if the user had previously liked
        if timepost.likes.filter(id=request.user.id).exists():
            timepost.likes.remove(request.user)
        timepost.dislikes.add(request.user)
    
    # Redirect to the 'next' URL, or default to 'home' if not provided
    next_url = request.GET.get('next', 'home')
    return redirect(next_url)

@login_required
def delete_timepost(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    
    # Check if the user has permission to delete the post (owner or superuser)
    if timepost.user == request.user or request.user.is_superuser:
        if request.method == 'POST':
            timepost.delete()
            messages.success(request, 'Your TimePost was deleted successfully.')
        else:
            messages.error(request, "Invalid request method.")
    else:
        messages.error(request, "You don't have permission to delete this post.")
    
    # Redirect to the next URL or home if none provided
    next_url = request.GET.get('next', 'home')
    return redirect(next_url)

@login_required
def edit_timepost(request, pk):
    timepost = get_object_or_404(TimePost, pk=pk)

    # Ensure that only the post's owner or a superuser can edit the post
    if request.user == timepost.user or request.user.is_superuser:
        if request.method == 'POST':
            form = TimePostForm(request.POST, instance=timepost)
            if form.is_valid():
                form.save()
                messages.success(request, 'The post was updated successfully.')

                # Get the 'next' URL, fallback to 'home' if not provided
                next_url = request.POST.get('next', 'home')
                return redirect(next_url)
        else:
            form = TimePostForm(instance=timepost)
    else:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('home')

    # Get the 'next' parameter to pass it back to the form in the template
    next_url = request.GET.get('next', 'home')

    return render(request, 'edit_timepost.html', {
        'form': form,
        'timepost': timepost,
        'next_url': next_url
    })

def search(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')
        if query:
            results = Profile.objects.filter(user__username__icontains=query)
        else:
            results = Profile.objects.none()
        return render(request, 'home/search.html', {
            'results': results,
            'user': request.user,
            'query': query
        })
    else:
        return redirect('login')

@login_required
def add_comment(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            Comment.objects.create(user=request.user, timepost=timepost, body=comment_body)
            messages.success(request, 'Your comment was posted successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    # Count the comments for this TimePost
    comment_count = Comment.objects.filter(timepost=timepost).count()
    
    # Get the `next` parameter from the request, default to 'home' if not provided
    next_url = request.GET.get('next', 'home')

    # If `next` is an actual URL, we can redirect to that
    # Reverse the URL if it's a named URL pattern
    try:
        redirect_url = reverse(next_url)
    except:
        # If `next` is already a path (e.g., /user/profile/), skip reversing
        redirect_url = next_url
    
    return redirect(f"{redirect_url}?comment_count={comment_count}")

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            comment.body = comment_body
            comment.save()
            messages.success(request, 'Your comment was updated successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)

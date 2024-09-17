from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, NoReverseMatch
from django.contrib import messages
from home.models import TimePost, Comment
from user.models import Profile
from .forms import TimePostForm


def index(request):
    # Handle authenticated users creating TimePosts
    if request.user.is_authenticated:
        form = TimePostForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            timepost = form.save(commit=False)
            timepost.user = request.user
            timepost.save()
            messages.success(request, 'Your TimePost was created successfully')
            return redirect(request.GET.get('next', 'home'))

        # Display all TimePosts in descending order
        timeposts = TimePost.objects.all().order_by('-created_at')
        return render(request, 'home/index.html', {
            'timeposts': timeposts,
            'form': form
        })
    else:
        # For unauthenticated users, just show TimePosts
        timeposts = TimePost.objects.all().order_by('-created_at')
        return render(request, 'home/index.html', {
            'timeposts': timeposts
        })


@login_required
def follow(request, pk):
    # Follow a user by their profile ID
    profile = get_object_or_404(Profile, user_id=pk)
    request.user.profile.follow.add(profile)
    request.user.profile.save()
    messages.success(request, f'You are now following {profile.user.username}')
    return redirect(request.POST.get('next', 'home'))


@login_required
def unfollow(request, pk):
    # Unfollow a user by their profile ID
    profile = get_object_or_404(Profile, user_id=pk)
    request.user.profile.follow.remove(profile)
    request.user.profile.save()
    messages.success(request, f'You have unfollowed {profile.user.username}')
    return redirect(request.POST.get('next', 'home'))


@login_required
def timepost_like(request, pk):
    # Toggle like status on a TimePost
    timepost = get_object_or_404(TimePost, id=pk)

    if timepost.likes.filter(id=request.user.id).exists():
        timepost.likes.remove(request.user)
    else:
        if timepost.dislikes.filter(id=request.user.id).exists():
            timepost.dislikes.remove(request.user)
        timepost.likes.add(request.user)

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)


@login_required
def timepost_dislike(request, pk):
    # Toggle dislike status on a TimePost
    timepost = get_object_or_404(TimePost, id=pk)

    if timepost.dislikes.filter(id=request.user.id).exists():
        timepost.dislikes.remove(request.user)
    else:
        if timepost.likes.filter(id=request.user.id).exists():
            timepost.likes.remove(request.user)
        timepost.dislikes.add(request.user)

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)


@login_required
def delete_timepost(request, pk):
    # Delete a TimePost if the user is the owner or a superuser
    timepost = get_object_or_404(TimePost, id=pk)

    if timepost.user == request.user or request.user.is_superuser:
        if request.method == 'POST':
            timepost.delete()
            messages.success(
                request, 'Your TimePost was deleted successfully.'
            )
        else:
            messages.error(request, "Invalid request method.")
    else:
        messages.error(
            request, "You don't have permission to delete this post."
        )

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)


@login_required
def edit_timepost(request, pk):
    # Edit a TimePost if the user is the owner or a superuser
    timepost = get_object_or_404(TimePost, pk=pk)

    if request.user == timepost.user or request.user.is_superuser:
        if request.method == 'POST':
            form = TimePostForm(request.POST, instance=timepost)
            if form.is_valid():
                form.save()
                messages.success(request, 'The post was updated successfully.')
                next_url = request.POST.get('next', 'home')
                return redirect(next_url)
        else:
            form = TimePostForm(instance=timepost)
    else:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('home')

    next_url = request.GET.get('next', 'home')
    return render(request, 'edit_timepost.html', {
        'form': form,
        'timepost': timepost,
        'next_url': next_url
    })


def search(request):
    # Perform a search for profiles based on username
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
    # Add a comment to a TimePost
    timepost = get_object_or_404(TimePost, id=pk)

    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            Comment.objects.create(
                user=request.user, timepost=timepost, body=comment_body
            )
            messages.success(request, 'Your comment was posted successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')

    comment_count = Comment.objects.filter(timepost=timepost).count()
    next_url = request.GET.get('next', 'home')
    try:
        redirect_url = reverse(next_url)
    except NoReverseMatch:
        redirect_url = next_url

    return redirect(f"{redirect_url}?comment_count={comment_count}")


@login_required
def delete_comment(request, comment_id):
    # Delete a comment by its ID
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)


@login_required
def edit_comment(request, comment_id):
    # Edit a comment by its ID
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

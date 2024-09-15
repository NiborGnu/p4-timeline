from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
def unfollow(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    request.user.profile.follow.remove(profile)
    request.user.profile.save()
    messages.success(request, f'You have unfollowed {profile.user.username}')
    return redirect(request.GET.get('next', 'home'))

@login_required
def follow(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    request.user.profile.follow.add(profile)
    request.user.profile.save()
    messages.success(request, f'You are now following {profile.user.username}')
    return redirect(request.GET.get('next', 'home'))

@login_required
def timepost_like(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.likes.filter(id=request.user.id).exists():
        timepost.likes.remove(request.user)
    else:
        if timepost.dislikes.filter(id=request.user.id).exists():
            timepost.dislikes.remove(request.user)
        timepost.likes.add(request.user)
    return redirect(request.GET.get('next', 'home'))

@login_required
def timepost_dislike(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.dislikes.filter(id=request.user.id).exists():
        timepost.dislikes.remove(request.user)
    else:
        if timepost.likes.filter(id=request.user.id).exists():
            timepost.likes.remove(request.user)
        timepost.dislikes.add(request.user)
    return redirect(request.GET.get('next', 'home'))

@login_required
def delete_timepost(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.user == request.user:
        timepost.delete()
        messages.success(request, 'Your TimePost was deleted successfully')
    else:
        messages.error(request, "You don't have permission to delete this post.")
    return redirect(request.GET.get('next', 'home'))

@login_required
def edit_timepost(request, pk):
    timepost = get_object_or_404(TimePost, id=pk)
    if timepost.user == request.user or request.user.is_superuser:
        form = TimePostForm(request.POST or None, instance=timepost)
        if request.method == 'POST':
            if form.is_valid():
                timepost = form.save(commit=False)
                timepost.user = request.user
                timepost.save()
                messages.success(request, 'The TimePost was updated successfully.')
                return redirect(request.GET.get('next', 'home'))
        return render(request, 'home/edit_timepost.html', {
            'form': form, 
            'timepost': timepost
        })
    else:
        messages.error(request, 'You do not have permission to edit this TimePost.')
        return redirect('home')

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
    comment_count = Comment.objects.filter(timepost=timepost).count()
    return redirect(f"{request.GET.get('next', 'home')}?comment_count={comment_count}")

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    return redirect(request.GET.get('next', 'home'))

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Comment edited successfully.')
                return redirect(request.GET.get('next', 'home'))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'home/edit_comment.html', {
            'form': form, 
            'comment': comment
        })
    else:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('home')

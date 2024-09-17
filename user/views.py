from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from home.models import TimePost
from user.models import Profile


@login_required
def users(request):
    """
    List all users except the current logged-in user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template showing users.
    """
    # List all users except the current user
    users = Profile.objects.exclude(user=request.user)
    return render(
        request,
        'user/users.html',
        {'users': users}
    )


@login_required
def profile(request, pk):
    """
    View profile details and handle follow/unfollow actions.

    Args:
        request: The HTTP request object.
        pk: The primary key of the user whose profile is viewed.

    Returns:
        HttpResponse: Rendered HTML template showing the profile and
        their timeposts.
    """
    # Get profile and timeposts of the user
    profile = get_object_or_404(Profile, user_id=pk)
    timeposts = TimePost.objects.filter(user_id=pk).order_by('-created_at')

    if request.method == 'POST':
        current_user_profile = request.user.profile
        action = request.POST.get('follow')

        if action == 'unfollow':
            current_user_profile.follow.remove(profile)
            messages.success(
                request,
                f'You have unfollowed {profile.user.username}'
            )
        else:
            current_user_profile.follow.add(profile)
            messages.success(
                request,
                f'You are now following {profile.user.username}'
            )
        return redirect('profile', pk=pk)

    return render(
        request,
        'user/profile.html',
        {'profile': profile, 'timeposts': timeposts}
    )


@login_required
def followers(request, pk):
    """
    List followers of a user, excluding the current user.

    Args:
        request: The HTTP request object.
        pk: The primary key of the user whose followers are listed.

    Returns:
        HttpResponse: Rendered HTML template showing the followers.
    """
    # List followers of the user, excluding the current user
    profile = get_object_or_404(Profile, user_id=pk)
    followers_list = profile.followed_by.exclude(user_id=request.user.id)

    if request.user.id == pk:
        return render(
            request,
            'user/followers.html',
            {'followers': followers_list}
        )
    else:
        messages.error(
            request,
            'That is not your followers page'
        )
        return redirect('home')


@login_required
def follows(request, pk):
    """
    List users the profile is following, excluding the current user.

    Args:
        request: The HTTP request object.
        pk: The primary key of the user whose following list is shown.

    Returns:
        HttpResponse: Rendered HTML template showing the follows.
    """
    # List users the profile is following, excluding the current user
    profile = get_object_or_404(Profile, user_id=pk)
    follows_list = profile.follow.exclude(user_id=request.user.id)

    if request.user.id == pk:
        return render(
            request,
            'user/follows.html',
            {'follows': follows_list}
        )
    else:
        messages.error(
            request,
            'That is not your follows page'
        )
        return redirect('home')


@login_required
def delete_profile(request, profile_id):
    """
    Handle profile deletion by user or superuser.

    Args:
        request: The HTTP request object.
        profile_id: The ID of the profile to be deleted.

    Returns:
        HttpResponse: Redirects to home or users page after deletion.
    """
    # Handle profile deletion by user or superuser
    profile = get_object_or_404(Profile, id=profile_id)

    if request.user != profile.user and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        # Delete all TimePosts and related data
        timeposts = TimePost.objects.filter(user=profile.user)
        for timepost in timeposts:
            timepost.likes.clear()
            timepost.dislikes.clear()
            timepost.comments.all().delete()
            timepost.delete()

        if profile.user == request.user:
            profile.user.delete()
            logout(request)
            messages.success(
                request,
                'Your profile has been deleted successfully.'
            )
            return redirect('home')
        else:
            profile.user.delete()
            messages.success(
                request,
                f'The profile for {profile.user.username} has been deleted '
                'successfully.'
            )
            return redirect('users')

    return redirect('home')

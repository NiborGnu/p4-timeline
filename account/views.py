from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Error logging in. Please try again')
            return redirect('login')
    return render(request, 'account/login.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    if request.method == 'POST':
        if 'logout-no' in request.POST:
            messages.info(request, 'Logout canceled.')
            return redirect('home')
        else:
            logout(request)
            messages.success(
                request, 'You have been logged out. Hope to see you soon!'
                )
            response = redirect('home')
            # Set additional cache control headers if needed
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
    return render(request, 'account/logout.html')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "You have successfully registered! Welcome!"
                )
            return redirect('home')
    return render(request, "account/register.html", {'form': form})


@login_required
def update_user(request):
    # Ensure the user is authenticated
    current_user = get_object_or_404(User, id=request.user.id)
    form = SignUpForm(request.POST or None, instance=current_user)
    if form.is_valid():
        form.save()
        # Re-login the user to update session details
        login(request, current_user)
        messages.success(request, 'Your profile was updated successfully')
        return redirect('home')
    return render(request, 'account/edit_profile.html', {'form': form})

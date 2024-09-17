from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User


def login_user(request):
    # Handle POST request for user login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Authentication successful, log in the user
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            # Authentication failed, show error message and redirect
            messages.error(request, 'Error logging in. Please try again')
            return redirect('login')

    # Handle GET request: Render the login page
    return render(request, 'account/login.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    # Handle POST request for user logout
    if request.method == 'POST':
        if 'logout-no' in request.POST:
            # Logout canceled, show info message and redirect
            messages.info(request, 'Logout canceled.')
            return redirect('home')
        else:
            # Log out the user and show success message
            logout(request)
            messages.success(
                request, 'You have been logged out. Hope to see you soon!'
            )
            response = redirect('home')
            # Set additional cache control headers
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

    # Handle GET request: Render the logout confirmation page
    return render(request, 'account/logout.html')


def register_user(request):
    # Initialize the signup form
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the new user and log them in
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "You have successfully registered! Welcome!"
            )
            return redirect('home')

    # Handle GET request or invalid POST: Render the registration page
    return render(request, "account/register.html", {'form': form})


@login_required
def update_user(request):
    # Ensure the user is authenticated and fetch their details
    current_user = get_object_or_404(User, id=request.user.id)
    form = SignUpForm(request.POST or None, instance=current_user)

    if form.is_valid():
        # Save the updated user details and re-login the user
        form.save()
        login(request, current_user)
        messages.success(request, 'Your profile was updated successfully')
        return redirect('home')

    # Handle GET request or invalid POST: Render the profile update page
    return render(request, 'account/edit_profile.html', {'form': form})

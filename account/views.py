from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User


def login_required_custom(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('account/login_required.html')
            return HttpResponse(template.render({}, request))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_user(request):
    """
    Handle user login. On POST, authenticate and log in the user.
    On GET, render the login page.
    """
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


@login_required_custom
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    """
    Handle user logout. On POST, log out the user or cancel logout.
    On GET, render the logout confirmation page.
    """
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
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

    return render(request, 'account/logout.html')


def register_user(request):
    """
    Handle user registration. On POST, validate and save the user.
    On GET or invalid POST, render the registration page.
    """
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "You have successfully registered! Welcome!"
            )
            return redirect('home')

    return render(request, "account/register.html", {'form': form})


@login_required_custom
def update_user(request):
    """
    Handle user profile update. On POST, save updates and re-login user.
    On GET or invalid POST, render the profile update page.
    """
    current_user = get_object_or_404(User, id=request.user.id)
    form = SignUpForm(request.POST or None, instance=current_user)

    if form.is_valid():
        form.save()
        login(request, current_user)
        messages.success(request, 'Your profile was updated successfully')
        return redirect('home')

    return render(request, 'account/edit_profile.html', {'form': form})

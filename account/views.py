from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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
            messages.success(request, 'Error logging in. Please try again')
            return redirect('login')
    else:
        return render(request, 'account/login.html')

def logout_user(request):
    if request.method == 'POST':
        if 'logout-no' in request.POST:  # If "No" button is clicked
            messages.info(request, 'Logout canceled.')
            return redirect('home')  # Redirect to home or any other page

        # If "Yes" button is clicked, log out the user
        logout(request)
        messages.success(request, 'You have been logged out. See you soon!')
        return redirect('home')  # Redirect to home or another page after logout

    return render(request, 'account/logout.html')

def register_user(request):
    return render(request, 'account/register.html')
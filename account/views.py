from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
            messages.success(request, 'Error logging in. Please try again')
            return redirect('login')
    else:
        return render(request, 'account/login.html')

def logout_user(request):
    if request.method == 'POST':
        if 'logout-no' in request.POST:  # If "No" button is clicked
            messages.info(request, 'Logout canceled.')
            return redirect('home')  # Redirect to home or any other page
        else: # If "Yes" button is clicked, log out the user
            logout(request)
            messages.success(request, 'You have been logged out. Hopes to see you soon!')
            return redirect('home')  # Redirect to home or another page after logout

    return render(request, 'account/logout.html')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "account/register.html", {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)  # Re-login the user to update session details
            messages.success(request, 'Your profile was updated successfully')
            return redirect('home')
        return render(request, 'account/edit_profile.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('login')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile


def index(request):
    return render(request, 'home/index.html')


def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'home/profiles.html', {'profiles': profiles})
    else: 
        messages.success(request, 'You must be logged in to view this page')
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'home/profile.html', {'profile': profile})
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')
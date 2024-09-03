from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    return render(request, 'account/login_user.html')

def register_user(request):
    return render(request, 'account/register_user.html')

def logout_user(request):
    return render(request, 'account/logout_user.html')
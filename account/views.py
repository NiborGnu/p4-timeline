from django.shortcuts import render


def login(request):
    return render(request, 'account/login_user.html')

def register(request):
    return render(request, 'account/register_user.html')

def logout(request):
    return render(request, 'account/logout_user.html')
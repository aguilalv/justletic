""" Views to manage Justletic user accounts """
import django.contrib.auth

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate

LOGIN_ERROR = 'Ooops, wrong user or password'

def login(request):
    """Check email and password received form a POST request and log user in"""
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('home')
    return render(request, 'home.html', {'error':LOGIN_ERROR})

def logout(request):
    """Log out user currently logged in"""
    auth_logout(request)
    return redirect(reverse('home'))

def create_new_strava_user(request):
    user_model = django.contrib.auth.get_user_model()
    
    email = request.POST['email']
    user = user_model.objects.create_user(email=email)

    auth_login(request, user)

    return redirect('https://www.strava.com/oauth/authorize?client_id=15873&redirect_uri=http://127.0.0.1:8000/users/stravatokenexchange&response_type=code&scope=view_private')

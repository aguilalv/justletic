""" Views to manage Justletic user accounts """
from django.shortcuts import render, redirect
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
    return render(request, 'home.html')

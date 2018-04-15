from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate

LOGIN_ERROR = 'Ooops, wrong user or password'

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email,password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('home')
    else:
        return render(request,'home.html',{'error':LOGIN_ERROR})

def logout(request):
    auth_logout(request)
    return render(request,'home.html')

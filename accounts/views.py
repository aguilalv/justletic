""" Views to manage Justletic user accounts """
import os
import django.contrib.auth
from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate

from keys.forms import HeroForm
from utils.strava_utils import strava_oauth_code_request_url

LOGIN_ERROR = "Ooops, wrong user or password"


def login(request):
    """Check email and password received form a POST request and log user in"""
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(username=email, password=password)
    if user is not None:
        auth_login(request, user)
    else:
        messages.add_message(request, messages.ERROR, LOGIN_ERROR)
    return render(request, "home.html")


def logout(request):
    """Log out user currently logged in"""
    auth_logout(request)
    return redirect(reverse("home"))


def create_new_strava_user(request):
    form = HeroForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        user_model = django.contrib.auth.get_user_model()
        user = user_model.objects.create_user(username=email, email=email)
        auth_login(request, user)
    else:
        return render(request, "home.html", {"form": form})

    return redirect(strava_oauth_code_request_url())

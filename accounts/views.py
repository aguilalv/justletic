""" Views to manage Justletic user accounts """
import os
import logging
from structlog import wrap_logger

import django.contrib.auth

from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate

from keys.forms import HeroForm
from utils.strava_utils import strava_oauth_code_request_url

LOGIN_ERROR = "Ooops, wrong user or password"

log = logging.getLogger(__name__)
logger = wrap_logger(log)

def login(request):
    """Check email and password received form a POST request and log user in"""
    global logger 
    #logger = logger.new()
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(username=email, password=password)
    if user is not None:
        logger = logger.bind(user=user.email)
        logger.info("Successful login")
        auth_login(request, user)
    else:
        logger = logger.bind(email=email)
        logger = logger.bind(password=password)
        logger.info("Failed login attempt")
        messages.add_message(request, messages.ERROR, LOGIN_ERROR)
    return render(request, "home.html")

def logout(request):
    """Log out user currently logged in"""
    global logger
    auth_logout(request)
    logger.info("Logout")
    return redirect(reverse("home"))


def create_new_strava_user(request):
    global logger
    form = HeroForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        user_model = django.contrib.auth.get_user_model()
        user = user_model.objects.create_user(username=email, email=email)
        logger = logger.bind(user=user.email)
        logger.info("User created")
        
        auth_login(request, user)
        logger.info("Successful login")
    else:
        return render(request, "home.html", {"form": form})

    return redirect(strava_oauth_code_request_url())

def change_password(request):
    """Change password for logged in user"""
    next_page = request.POST["next"]
    password = request.POST["password"]
    logged_in_user = request.user
    logged_in_user.set_password(password) 
    logged_in_user.save()
    return redirect(next_page)


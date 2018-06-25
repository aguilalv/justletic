""" Views to manage Justletic user accounts """
import os
import logging
from structlog import wrap_logger

import django.contrib.auth

from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate, update_session_auth_hash

from .forms import LoginForm

from keys.forms import HeroForm
from utils.strava_utils import strava_oauth_code_request_url

LOGIN_ERROR = "Ooops, wrong user or password"

log = logging.getLogger(__name__)
logger = wrap_logger(log)

def login(request):
    """Check email and password received form a POST request and log user in"""
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 
            "login.html",
            {"login_form": login_form},
        )
    
    global logger
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        email = login_form.cleaned_data.get("email")
        password = login_form.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            logger = logger.new()
            logger = logger.bind(user=user.email)
            logger.info("Successful login")
            auth_login(request, user)
        else:
            logger = logger.bind(email=email)
            logger = logger.bind(password=password)
            logger.info("Failed login attempt")
            messages.add_message(request, messages.ERROR, LOGIN_ERROR)
    return render(request, 
        "home.html",
        {"login_form": login_form},
    )

def logout(request):
    """Log out user currently logged in"""
    global logger
    auth_logout(request)
    logger.info("Logout")
    return redirect(reverse("home"))


def create_new_strava_user(request):
    global logger
    hero_form = HeroForm(request.POST)
    login_form = LoginForm()
    if hero_form.is_valid():
        email = hero_form.cleaned_data.get("email")
        user_model = django.contrib.auth.get_user_model()
        user = user_model.objects.create_user(username=email, email=email)
        logger = logger.bind(user=user.email)
        logger.info("User created")
        
        auth_login(request, user)
        logger.info("Successful login")
    else:
        return render(
            request,
            "home.html", 
            {"hero_form": hero_form, "login_form": login_form}
        )

    return redirect(strava_oauth_code_request_url())

def change_password(request):
    """Change password for logged in user"""
    global logger
    next_page = request.POST["next"]
    password = request.POST["password"]
    logged_in_user = request.user
    logger = logger.bind(user=logged_in_user.email)
    logged_in_user.set_password(password) 
    logged_in_user.save()
    update_session_auth_hash(request, logged_in_user) 
    logger.info("Password changed") 
    return redirect(next_page)


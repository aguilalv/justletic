""" Views to manage Keys for Justletic external services """
import requests
import os
import logging
from structlog import wrap_logger

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .forms import HeroForm
from .models import Key

from utils.strava_utils import STRAVA_AUTH_ERROR
from utils.strava_utils import exchange_strava_code, get_strava_activities
from accounts.forms import LoginForm


log = logging.getLogger(__name__)
logger = wrap_logger(log)

def home_page(request):
    """Render Justletic home page"""
    hero_form = HeroForm()
    login_form = LoginForm()
    return render(request, "home.html", {"hero_form": hero_form, "login_form": login_form})

def strava_token_exchange(request):
    """Receives Strava authorisation code and sends request for user token"""
    global logger
    logged_in_user = request.user
    logger = logger.bind(user=logged_in_user.email) 

    code = request.GET.get("code")
    token, strava_id = exchange_strava_code(code)

    if not token or not strava_id:
        messages.add_message(request, messages.ERROR, STRAVA_AUTH_ERROR)
        logger.info("Received Strava error in token exchange")
        return render(request, "home.html")

    new_key = Key(user=logged_in_user, token=token, strava_id=strava_id)
    new_key.save()
    logger.info("Access to Strava authorised")

    activities = get_strava_activities(token)
    if activities:
        logger.info("Strava activity summary received") 
        return render(
            request,
            "congratulations.html",
            {"last_activity_distance": activities[0].get("distance") / 1000},
        )
    else:
        messages.add_message(request, messages.ERROR, STRAVA_AUTH_ERROR)
        logger.info("Received Strava error for activity summary")
        return render(request, "home.html")

""" Views to manage Keys for Justletic external services """
import requests
import os
import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .forms import HeroForm
from .models import Key

from utils.strava_utils import STRAVA_AUTH_ERROR
from utils.strava_utils import exchange_strava_code, get_strava_activities

logger = logging.getLogger(__name__)

def home_page(request):
    """Render Justletic home page"""
    form = HeroForm()
    
    logger.info("keys.views.home - end")
    return render(request, "home.html", {"form": form})


def strava_token_exchange(request):
    """Receives Strava authorisation code and sends request for user token"""
    code = request.GET.get("code")

    token, strava_id = exchange_strava_code(code)

    if not token or not strava_id:
        messages.add_message(request, messages.ERROR, STRAVA_AUTH_ERROR)
        logger.info("keys.views.stravatokenexchange - error")
        return render(request, "home.html")

    logged_in_user = request.user
    new_key = Key(user=logged_in_user, token=token, strava_id=strava_id)
    new_key.save()

    activities = get_strava_activities(token)

    if activities:
        logger.info("keys.views.stravatokenexchange - end")
        return render(
            request,
            "congratulations.html",
            {"last_activity_distance": activities[0].get("distance") / 1000},
        )
    else:
        messages.add_message(request, messages.ERROR, STRAVA_AUTH_ERROR)
        logger.info("keys.views.stravatokenexchange - error")
        return render(request, "home.html")

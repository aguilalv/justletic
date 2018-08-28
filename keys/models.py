""" Models to store Keys and tokens for authenticated services """

from django.db import models
from django.contrib import auth


class Key(models.Model):
    STRAVA = 'STR'
    SPOTIFY = 'SPO'
    SERVICE_CHOICES = (
        (STRAVA, 'Strava'),
        (SPOTIFY, 'Spotify'),
    )
    
    user_model = auth.get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, default=None)
    refresh_token = models.CharField(max_length=50, default=None, blank=True)
    strava_id = models.CharField(max_length=50, default=None, blank=True)
    service = models.CharField(
        max_length=3,
        choices=SERVICE_CHOICES,
        default=None,
    )

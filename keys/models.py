""" Models to store Keys and tokens for authenticated services """

from django.db import models
from django.contrib import auth

class Key(models.Model):
    user_model = auth.get_user_model()

    user = models.ForeignKey(user_model,on_delete=models.CASCADE)
    token = models.CharField(max_length=50,default=None)
    strava_id = models.CharField(max_length=50,default=None)

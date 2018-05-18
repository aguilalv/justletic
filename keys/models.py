""" Models to store Keys and tokens for authenticated services """

from django.db import models
from accounts.models import User

class Key(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=50,default=None)
    strava_id = models.CharField(max_length=50,default=None)

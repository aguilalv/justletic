from django.db import models


class User(models.Model):
    email = models.TextField(default='')

class Key(models.Model):
    value = models.TextField(default='')    
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

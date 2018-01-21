from django.db import models

class Key(models.Model):
    email = models.TextField(default='')
    value = models.TextField(default='')


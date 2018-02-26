from django.db import models
from django.urls import reverse

class User(models.Model):
    email = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('view_user', args=[self.id])

class Key(models.Model):
    value = models.TextField(default='')    
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

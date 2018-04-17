""" Models to store keys for Justletic external services"""
from django.db import models
from django.urls import reverse

class User(models.Model):

    """TO BE DEPRECATED: Tests for Keys internal User models"""

    email = models.TextField(default='')

    def get_absolute_url(self):
        """ Return the url to view details of this model"""
        return reverse('view_user', args=[self.id])

class Key(models.Model):

    """Model to store Keys for external services"""

    value = models.TextField(default='')
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

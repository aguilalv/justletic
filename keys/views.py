""" Views to manage Keys for Justletic external services """
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Key, User

EMAIL_ERROR = "You need to enter a valid email"

def home_page(request):
    """Render Justletic home page"""
    return render(request, 'home.html')

def new_user(request):
    """TO BE DEPRECATED: Create a Keys user account"""
    user = User()
    user.email = request.POST['email']
    try:
        user.full_clean()
        user.save()
    except ValidationError:
        return render(request, 'home.html', {'error': EMAIL_ERROR})

    new_key = Key()
    new_key.value = request.POST['email'][0] + '1234'
    new_key.user = user
    new_key.save()

    return redirect('view_user', user.id)

def view_user(request, user_id):
    """TO BE DEPRECATED: Render details page for a Keys user account"""
    user = User.objects.get(id=user_id)
    keys = Key.objects.filter(user=user)

    return render(request, 'user.html', {'keys': keys, 'user': user})

def add_service(request, user_id):
    """Associate a service key to a user account and redirect to its detail view

    Args:
        request (django.http.HttpRequest): Django request generating the call
        user_id (int): Id for the user to associate key with

    """
    user = User.objects.get(id=user_id)

    new_key = Key()
    new_key.value = user.email[1] + '1234'
    new_key.user = user
    new_key.save()

    return redirect('view_user', user_id)

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Key, User

def home_page(request):
    return render(request,'home.html')

def new_user(request):
    new_user = User()
    new_user.email = request.POST['email']
    new_user.save()

    new_key = Key()
    new_key.value = 'e1234'
    new_key.user = new_user
    new_key.save()
    return redirect('/users/the-only-user/')

def view_user(request):
    user = User.objects.all()[0]
    keys = Key.objects.all()
    return render(request,'user.html', {'keys': keys, 'user': user})

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Key

def home_page(request):
    
    if request.method == 'POST':
        new_key = Key()
        new_key.email = request.POST['email']
        new_key.value = 'e1234'
        new_key.save()

        return redirect('/users/the-only-user/')

    return render(request,'home.html')

def view_user(request):
    keys = Key.objects.all()
    return render(request,'user.html', {'keys': keys})

from django.shortcuts import render, redirect
from django.http import HttpResponse

from stravaAuth.models import Key

def home_page(request):
    
    if request.method == 'POST':
        new_key = Key()
        new_key.email = request.POST['email']
        new_key.save()

        return redirect('/')

    return render(request,'home.html')


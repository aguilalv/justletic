from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from .models import Key, User

EMAIL_ERROR = "You need to enter a valid email"

def home_page(request):
    return render(request,'home.html')

def new_user(request):
    new_user = User()
    new_user.email = request.POST['email']
    try:
        new_user.full_clean()
        new_user.save()
    except ValidationError:
        return render(request,'home.html',{'error': EMAIL_ERROR})

    new_key = Key()
    new_key.value = request.POST['email'][0] + '1234'
    new_key.user = new_user
    new_key.save()

    return redirect('view_user', new_user.id)

def view_user(request, user_id):
    user = User.objects.get(id=user_id)
    keys = Key.objects.filter(user=user)

    return render(request,'user.html', {'keys': keys, 'user': user})
            
def add_service(request, user_id):
    user = User.objects.get(id=user_id)
    
    new_key = Key()
    new_key.value = user.email[1] + '1234'
    new_key.user = user
    new_key.save()
    
    return redirect('view_user', user_id)

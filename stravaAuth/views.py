from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    if request.method == 'POST':
        return render(request, 'home.html', {
            'email_text': request.POST['email'],
        })

    return render(request,'home.html')


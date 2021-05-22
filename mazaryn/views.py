from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):

    user = request.user
    hello = 'Hi, over there'

    context = {
        'user': user,
        'greetings': hello,
    }
    return render(request,'main/home.html', context)

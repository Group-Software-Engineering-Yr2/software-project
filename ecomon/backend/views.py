from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here

def example_view(request):
    return HttpResponse('Hello, World!')

def home(request):
    return render(request, 'homePage/homePage.html')

def packs(request):
    return HttpResponse('temp')

def scanner(request):
    return HttpResponse('temp')

def profile(request):
    return render(request, 'profile/profile.html')

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')

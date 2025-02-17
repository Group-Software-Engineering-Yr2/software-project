from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def home(request):
    return render(request, 'homePage/homePage.html')

@login_required
def packs(request):
    return HttpResponse('temp')

@login_required
def scanner(request):
    return HttpResponse('temp')

@login_required
def profile(request):
    return HttpResponse('temp')

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')
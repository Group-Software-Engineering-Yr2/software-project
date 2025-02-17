from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here

def home(request):
    return render(request, 'backend/homePage.html')

def packs(request):
    return HttpResponse('temp')

def scanner(request):
    return HttpResponse('temp')

def profile(request):
    return HttpResponse('temp')

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')
    
# @login_required
def render_scanner(request):
    return render(request, 'backend/scanner.html')

# @login_required
def render_gym_battle(request, gym_id):
    return render(request, "backend/gym_battle.html", {"gym_id": gym_id})

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Card, PlayerCards

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
    cards = Card.objects.all().order_by('card_type')
    players_cards = PlayerCards.objects.all()
    context = {
        "cards": cards,
        "player_cards": players_cards,
        "user": request.user,  # Pass the user object to the template
    }
    return render(request, 'profile/profile.html', context)

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')

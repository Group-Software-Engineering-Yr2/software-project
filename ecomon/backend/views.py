from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Card, PlayerCards
from django.core import serializers

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
    cards = Card.objects.all()
    playerCards = PlayerCards.objects.all() 
    context = {
        "cards": cards,  # Original QuerySet for counting
        "cards_data": serializers.serialize('json', cards),  # Serialized data for JavaScript
        "playerCards": playerCards,  # Original QuerySet
        "player_cards_data": serializers.serialize('json', playerCards)  # Serialized data for JavaScript
    }
    return render(request, 'profile/profile.html', context)

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Card, PlayerCards
from django.core import serializers
from django.http import JsonResponse

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
    return render(request, "profile/profile.html")


def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')

def get_cards(request):
    cards = list(Card.objects.values("name", "card_type", "image"))
    return JsonResponse({"cards": cards})

def get_player_cards(request):
    player_cards = list(PlayerCards.objects.filter(player=request.user).values(
        "card__name",
        "use_count"
    ))
    formatted_player_cards = [
        {
            "name": pc["card__name"],
            "use_count": pc["use_count"]
        } for pc in player_cards
    ]
    return JsonResponse({"player_cards": formatted_player_cards})
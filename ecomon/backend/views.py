from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .pack_service import get_pack_count, reduce_user_pack_count,generate_pack, add_player_cards
from .models import Gym

# Create your views here

@login_required
def home(request):
    return render(request, 'backend/homePage.html')

@login_required
def profile(request):
    return HttpResponse('temp')

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')

@login_required
def open_pack(request):
    ''' Checks if there is a pack to open and shows the user confirmation'''
    pack_count = get_pack_count(request.user)
    # If packs simulate the packs and display to user
    if pack_count > 0:
        return render(request, 'backend/packs/open_pack.html', {'pack_count': pack_count})
    return render(request, 'backend/packs/nopacks.html')

@login_required
def opening_pack(request):
    '''
    Actual logic for opening a pack
    '''
    pack_count = get_pack_count(request.user)
    if pack_count <= 0:
        return redirect('/packs')

    # If the user has a pack

    # Generate the cards
    pack_cards = generate_pack()
    # Add the cards to the user's collection (PlayerCards)
    add_player_cards(request.user, pack_cards)
    # Decrement pack count from the user's profile
    reduce_user_pack_count(request.user)
    # Show the user the cards they got

    card_images = [str(pack.image).replace('static/', '') for pack in pack_cards]
    return render(request, 'backend/packs/opening_pack.html', {'card_images': card_images})

# @login_required
def render_scanner(request):
    return render(request, 'backend/scanner.html')

# @login_required
def render_gym_battle(request, gym_id):
    try:
        gym = Gym.objects.get(id=gym_id)
    except Gym.DoesNotExist:
        # Todo update this to custom template
        return HttpResponse('Gym does not exist')
    
    return render(request, "backend/gym_battle.html", {"gym_id": gym_id})

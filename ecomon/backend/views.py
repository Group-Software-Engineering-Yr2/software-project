from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .pack_service import get_pack_count, reduce_user_pack_count,generate_pack, add_player_cards
from .models import Card, PlayerCards
from django.contrib.auth import logout


@login_required
def home(request):
    return render(request, 'backend/homePage.html')

@login_required
def profile(request):
    cards = Card.objects.all().order_by('card_type')
    players_cards = PlayerCards.objects.filter(player=request.user)  # Get logged-in user's cards
    # Get deck cards for the user
    deck_card_1 = request.user.profile.deck_card_1
    deck_card_2 = request.user.profile.deck_card_2
    deck_card_3 = request.user.profile.deck_card_3

    # Get the logo of the user's team (assuming team has a 'logo' field)
    team_logo = request.user.profile.team_name.icon if request.user.profile.team_name else None

    context = {
        "cards": cards,
        "player_cards": players_cards,
        "user": request.user,
        "wrapper_count": request.user.profile.wrapper_count,
        "deck_card_1": deck_card_1,
        "deck_card_2": deck_card_2,
        "deck_card_3": deck_card_3,
        "team_logo": team_logo,
    }
    return render(request, 'backend/profile/profile.html', context)

@login_required
def change_deck(request):
    cards = Card.objects.all().order_by('card_type')
    players_cards = PlayerCards.objects.filter(player=request.user)
    deck_card_1 = request.user.profile.deck_card_1
    deck_card_2 = request.user.profile.deck_card_2
    deck_card_3 = request.user.profile.deck_card_3

    context = {
        "cards": cards,
        "player_cards": players_cards,
        "user": request.user,
        "deck_card_1": deck_card_1,
        "deck_card_2": deck_card_2,
        "deck_card_3": deck_card_3,
    }
    return render(request, 'backend/profile/changeDeck.html', context)

@login_required
def update_deck(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        selected_cards = request.POST.getlist('selected_cards')
        # Clear existing deck
        user_profile.deck_card_1 = None
        user_profile.deck_card_2 = None
        user_profile.deck_card_3 = None
        # Add selected cards in order
        for i, card_name in enumerate(selected_cards[:3]):
            card = Card.objects.get(name=card_name)
            if i == 0:
                user_profile.deck_card_1 = card
            elif i == 1:
                user_profile.deck_card_2 = card
            elif i == 2:
                user_profile.deck_card_3 = card
                
        user_profile.save()
    return redirect('change_deck')



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


@login_required
def render_scanner(request):
    return render(request, 'backend/scanner.html')

@login_required
def render_gym_battle(request, gym_id):
    return render(request, "backend/gym_battle.html", {"gym_id": gym_id})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

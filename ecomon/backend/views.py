from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from accounts.player_service import get_player_deck, has_deck, add_players_pack
from accounts.models import Profile
from .pack_service import get_pack_count, reduce_user_pack_count,generate_pack, add_player_cards
from .gym_service import reset_profile_wrappers, update_gym_cards, update_owning_player, update_cooldown
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
    ''' 
    Endpoint for scanning the QR code
    '''
    try:
        gym = Gym.objects.get(id=gym_id)
    except Gym.DoesNotExist:
        # Todo update this to custom template
        return HttpResponse('Gym does not exist')
    # Check the cooldown of the gym

    # Ensure user is within the gym radius

    # Check if the user has the required cards to battle the gym
    # Redirect to select deck page otherwise


    return render(request, "backend/gym_battle.html", {"gym_id": gym_id})

# @login_required
def render_gym_view(request, gym_id):
    ''' 
    Endpoint for scanning the QR code
    '''
    try:
        gym = Gym.objects.get(id=gym_id)
        profile = Profile.objects.filter(user=gym.owning_player).first()
        owning_player_team = profile.team_name.name if profile else "No team"
        
        # Todo check to see if player has 3 cards in their deck
        # Retrive PlayerCards objects and their associated Card images
        player_deck_card1 = profile.deck_card_1.card.image.url if profile and profile.deck_card_1 else None
        player_deck_card2 = profile.deck_card_2.card.image.url if profile and profile.deck_card_2 else None
        player_deck_card3 = profile.deck_card_3.card.image.url if profile and profile.deck_card_3 else None
        
        # Todo change this default to be team fossil fuel icon mimicking the start of the day
        team_icon_url = static('images/teams/team_fossil_fuel.png')
        if profile and profile.team_name.icon:
            team_icon_url = profile.team_name.icon.url

        context = {
            "gym_id": gym_id,
            "gym_name": gym.name,
            "gym_fact": gym.fact,
            "gym_card1": gym.card1,
            "gym_card2": gym.card2,
            "gym_card3": gym.card3,
            "gym_owning_player": gym.owning_player,
            "gym_owning_player_team": owning_player_team,
            "gym_cooldown": gym.cooldown,
            "gym_team_icon": team_icon_url,
            "player_deck_card1": player_deck_card1,
            "player_deck_card2": player_deck_card2,
            "player_deck_card3": player_deck_card3
        }
    except Gym.DoesNotExist:
        # Todo update this to custom template
        return HttpResponse('Gym does not exist')

    return render(request, "backend/view_gym.html", context)

# @login_required
def render_gym_battle_lorenzo(request, gym_id):
    return render(request, "backend/gym_battle_lorenzo.html")

@login_required
def completed_gym_battle(request):
    '''
    Endpoint for processing the result of a gym battle
    Required GET parameters:
    - did_win: boolean indicating if the user won the gym battle
    - gym_id: the id of the gym the

    Example Request:
    host/gym-battle-completed?did_win=true&gym_id=1
    '''
    did_win = request.GET.get('did_win')
    gym_id = request.GET.get('gym_id')
    if did_win is None or gym_id is None:
        # todo update this to a custom template render
        return HttpResponse('Missing win condition and gym id', status=400)

    # Get the gym
    try:
        gym = Gym.objects.get(id=gym_id)
    except Gym.DoesNotExist:
        # todo update this to a custom template render
        return HttpResponse('Gym does not exist', status=404)
    
    # Ensure the user has a selected deck
    if not has_deck(request.user):
        return HttpResponse('User does not have a deck selected', status=400)

    # Reset the user's wrapper count to 0
    reset_profile_wrappers(request.user)

    # Process the result of the gym battle
    if did_win == 'true':
        player_collection_cards = get_player_deck(request.user)
        # Set the gym's cards & update the player's cards in use
        update_gym_cards(player_collection_cards, gym)
        # Upadte the owning player
        update_owning_player(gym, request.user)
        # Update the cooldown of the gym
        update_cooldown(gym)
        # Add a pack to the user's profile
        add_players_pack(request.user)

    # todo update this to a custom template render
    return HttpResponse('Gym battle result processed')
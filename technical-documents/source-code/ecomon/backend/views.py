import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.db import transaction
from accounts.player_service import get_player_deck, has_deck, add_players_pack
from accounts.models import Profile
from .pack_service import get_pack_count, reduce_user_pack_count,generate_pack, add_player_cards, increase_packs_opened
from .gym_service import reset_profile_wrappers, update_gym_cards, update_owning_player, update_cooldown, increase_win_count, increase_bins_emptied, reset_gym_player_cards
from .bin_service import is_bin_full, increment_wrapper_count
from .models import Gym, Card, PlayerCards,Team
from .achievement_service import check_and_award_achievements
from .models import Gym, Card, PlayerCards
from datetime import timedelta

@login_required
def home(request):
    gyms = list(Gym.objects.values('name', 'latitude', 'longitude'))

    # getting last allocation from DB
    last_pack_allocation = Profile.objects.get(user=request.user).last_pack_allocation

    # getting 3 days ago
    threeDaysAgo = timezone.now().date() - timedelta(days=3)
    last_pack_allocation = timezone.now().date()
    
    # checking if more than three days or more ago
    if threeDaysAgo >= last_pack_allocation:
        add_players_pack(request.user)
        
        # updating last allocated time (not gonna create a service file cuz it's one operation)
        profile = Profile.objects.get(user=request.user)
        profile.last_pack_allocation = timezone.now().date()
        profile.save()
        
    return render(request, 'backend/home/homePage.html', {'gyms': gyms})

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
    referer = request.META.get("HTTP_REFERER")

    # Store referrer only if it's not `change_deck` itself
    if referer and "change_deck" not in referer:
        request.session["original_referrer"] = referer

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
        "previous_page": request.session.get("original_referrer", "/view-gym")
    }
    return render(request, 'backend/profile/changeDeck.html', context)

@login_required
def update_deck(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        
        # Get the cards in the order they were selected using list in change Deck JS
        selected_cards = request.POST.getlist('selected_cards')
        card_order = request.POST.getlist('card_order')
        
        # If card_order is not provided or doesn't contain all cards, use selected_cards
        ordered_cards = []
        for card_name in card_order:
            if card_name in selected_cards and len(ordered_cards) < 3:
                ordered_cards.append(card_name)
            
        
        # Clear existing deck
        user_profile.deck_card_1 = None
        user_profile.deck_card_2 = None
        user_profile.deck_card_3 = None
        
        # Add selected cards in order
        for i, card_name in enumerate(ordered_cards[:3]):
            try:
                card = Card.objects.get(name=card_name)
                if i == 0:
                    user_profile.deck_card_1 = card
                elif i == 1:
                    user_profile.deck_card_2 = card
                elif i == 2:
                    user_profile.deck_card_3 = card
            except Card.DoesNotExist:
                # Skip if card doesn't exist
                continue
                
        user_profile.save()

        # Get stored referrer and remove from session to avoid possible looping
        original_referrer = request.session.pop("original_referrer", "/view-gym")
        return redirect(original_referrer)
            
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
    # Check if the user's bin is full
    if is_bin_full(request.user):
        return render(request, 'backend/packs/bin_full.html')
    # If packs simulate the packs and display to user
    if pack_count > 0:
        return render(request, 'backend/packs/open_pack.html', {'pack_count': pack_count})
    return render(request, 'backend/packs/nopacks.html')

def opening_pack(request):
    '''
    Actual logic for opening a pack
    '''
    # If the user has a pack
    pack_count = get_pack_count(request.user)
    if pack_count <= 0:
        return redirect('/packs')

    # If there bin is full
    if is_bin_full(request.user):
        return redirect('/packs')
    # Increment the wrapper
    increment_wrapper_count(request.user)
    # Generate the cards
    pack_cards = generate_pack()
    # Add the cards to the user's collection (PlayerCards)
    add_player_cards(request.user, pack_cards)
    # Decrement pack count from the user's profile
    reduce_user_pack_count(request.user)
    # Increase the packs opened count
    increase_packs_opened(request.user)
    # Check if they have reached an achievement milestone
    check_and_award_achievements(request.user, 'PACKS')
     # Show the user the cards they got
    card_images = [str(pack.image).replace('static/', '') for pack in pack_cards]
    return render(request, 'backend/packs/opening_pack.html', {'card_images': card_images})


@login_required
def render_scanner(request):
    '''
    Endpoint for opening up the scanner page to scan the QR code
    '''
    return render(request, 'backend/scanner/scanner.html')

@login_required
def render_gym_view(request, gym_id):
    ''' 
    Endpoint from scanning a gym QR code
    '''
    try:
        #Retrieve gym object and gym team with player object and player team
        gym = Gym.objects.get(id=gym_id)
        profile = Profile.objects.filter(user=request.user).first()
        owning_player_team = profile.team_name.name if profile else "No team"
        gym_team = gym.owning_player.profile.team_name.name if gym.owning_player else "No team"

        # Retrieve PlayerCards objects and their associated Card images
        player_deck_card1 = profile.deck_card_1.image.url if profile and profile.deck_card_1 else None
        player_deck_card2 = profile.deck_card_2.image.url if profile and profile.deck_card_2 else None
        player_deck_card3 = profile.deck_card_3.image.url if profile and profile.deck_card_3 else None
        
        # Gym owning has a profile and a team icon
        if gym.owning_player and gym.owning_player.profile.team_name.icon:
            team_icon_url = gym.owning_player.profile.team_name.icon.url

        # Get the gym's cooldown end time
        cooldown_end_time = gym.cooldown.timestamp() if gym.cooldown else 0

        # Context variables to pass to the template
        context = {
            "gym_id": gym_id,
            "gym_name": gym.name,
            "gym_fact": gym.fact,
            "gym_card1": gym.card1,
            "gym_card2": gym.card2,
            "gym_card3": gym.card3,
            "gym_owning_player": gym.owning_player,
            "owning_player_team": owning_player_team,
            "gym_cooldown": cooldown_end_time,
            "gym_team": gym_team,
            "gym_team_icon": team_icon_url,
            "player_deck_card1": player_deck_card1,
            "player_deck_card2": player_deck_card2,
            "player_deck_card3": player_deck_card3,
            "gym_latitude": gym.latitude,
            "gym_longitude": gym.longitude,
        }
    except Gym.DoesNotExist:
        # Redirect to gym not found page
        return redirect('gym-not-found')

    return render(request, "backend/battles/view_gym.html", context)

@login_required
def render_gym_battle(request, gym_id):
    '''Endpoint after player starts a battle with a gym'''
    # Get the gym object and player's profile
    try:
        gym = Gym.objects.get(id=gym_id)
        profile = Profile.objects.filter(user=request.user).first()
        username = request.user.username
        
        # Retrieve PlayerCards objects
        player_deck_card1 = profile.deck_card_1 if profile and profile.deck_card_1 else None
        player_deck_card2 = profile.deck_card_2 if profile and profile.deck_card_2 else None
        player_deck_card3 = profile.deck_card_3 if profile and profile.deck_card_3 else None

        # Retrieve Player's and Gym Owning teams
        user_team = profile.team_name.name if profile else "No team"
        gym_team = gym.owning_player.profile.team_name.name if gym.owning_player else "No team"
        
        # Apply battle benefits based on the user's team
        if user_team == "Recycle":
            if player_deck_card1 and player_deck_card1.card_type == 2:
                player_deck_card1.ability_power_1 += 10
                if player_deck_card1.ability_power_2 != 0:
                    player_deck_card1.ability_power_2 += 10
            if player_deck_card2 and player_deck_card2.card_type == 2:
                player_deck_card2.ability_power_1 += 10
                if player_deck_card2.ability_power_2 != 0:
                    player_deck_card2.ability_power_2 += 10
            if player_deck_card3 and player_deck_card3.card_type == 2:
                player_deck_card3.ability_power_1 += 10
                if player_deck_card3.ability_power_2 != 0:
                    player_deck_card3.ability_power_2 += 10
        elif user_team == "Reduce":
            gym.card1.ability_power_1 -= 5
            gym.card2.ability_power_1 -= 5
            gym.card3.ability_power_1 -= 5
            if gym.card1.ability_power_2 != 0:
                gym.card1.ability_power_2 -= 5
            if gym.card2.ability_power_2 != 0:
                gym.card2.ability_power_2 -= 5
            if gym.card3.ability_power_2 != 0:
                gym.card3.ability_power_2 -= 5
        
        # Apply battle benefits based on the gym's team
        if gym_team == "Recycle":
            if gym.card1.card_type == 2:
                gym.card1.ability_power_1 += 10
                if gym.card1.ability_power_2 != 0:
                    gym.card1.ability_power_2 += 10
            if gym.card2.card_type == 2:
                gym.card2.ability_power_1 += 10
                if gym.card2.ability_power_2 != 0:
                    gym.card2.ability_power_2 += 10
            if gym.card3.card_type == 2:
                gym.card3.ability_power_1 += 10
                if gym.card3.ability_power_2 != 0:
                    gym.card3.ability_power_2 += 10
        elif gym_team == "Reduce":
            if player_deck_card1 and player_deck_card2 and player_deck_card3:
                player_deck_card1.ability_power_1 -= 5
                player_deck_card2.ability_power_1 -= 5
                player_deck_card3.ability_power_1 -= 5
                if player_deck_card1.ability_power_2 != 0:
                    player_deck_card1.ability_power_2 -= 5
                if player_deck_card2.ability_power_2 != 0:
                    player_deck_card2.ability_power_2 -= 5
                if player_deck_card3.ability_power_2 != 0:
                    player_deck_card3.ability_power_2 -= 5
            

        # Context variables to pass to the template
        context = {
            "gym_id": gym_id,
            "username": username,
            "gym_card1": json.dumps(gym.card1.to_json()),
            "gym_card2": json.dumps(gym.card2.to_json()),
            "gym_card3": json.dumps(gym.card3.to_json()),
            "gym_owning_player": gym.owning_player,
            "player_deck_card1": json.dumps(player_deck_card1.to_json()),
            "player_deck_card2": json.dumps(player_deck_card2.to_json()),
            "player_deck_card3": json.dumps(player_deck_card3.to_json()),
            "user_team": user_team,
            "gym_team": gym_team,
        }

    except Gym.DoesNotExist:
        # Redirect to gym not found page
        return redirect('gym-not-found')
    
    return render(request, "backend/battles/gym_battle.html", context)

@login_required
def completed_gym_battle(request):
    '''
    Endpoint for processing the result of a gym battle
    Required GET parameters:
    - did_win: boolean indicating if the user won the gym battle
    - gym_id: the id of the gym

    Example Request:
    host/gym-battle-completed?did_win=true&gym_id=1
    '''
    # Get the GET parameters
    did_win = request.GET.get('did_win')
    gym_id = request.GET.get('gym_id')

    #get players deck
    player_deck_cards = get_player_deck(request.user)

    # Ensure the required parameters are present
    if not did_win or not gym_id:
        return redirect('missing-battle-condition')
    else:
        # Get the gym object and user's profile with context variables
        try:
            gym = Gym.objects.get(id=gym_id)
            username = request.user.username
            user_team = request.user.profile.team_name.name
            gym_name = Gym.objects.get(id=gym_id).name
            gym_previous_owner = Gym.objects.get(id=gym_id).owning_player
            gym_previous_owner_team = gym_previous_owner.profile.team_name.name

            context = {
                "did_win": did_win,
                "gym_id": gym_id,
                "username": username,
                "user_team": user_team,
                "gym_name": gym_name,
                "gym_previous_owner": gym_previous_owner,
                "gym_previous_owner_team": gym_previous_owner_team
            }

        # If the gym is not found, redirect to the gym not found page
        except Gym.DoesNotExist:
            return redirect('gym-not-found/')

        # Ensure the user has a selected deck
        if not has_deck(request.user):
            return redirect('battle-deck-empty/')

        # Get initial values for verification
        initial_bins_emptied = request.user.profile.bins_emptied

        # Reset wrappers and increase bins emptied
        reset_profile_wrappers(request.user)
        increase_bins_emptied(request.user)
        check_and_award_achievements(request.user, 'BINS')

        # Verify changes were saved
        request.user.profile.refresh_from_db()
        if request.user.profile.wrapper_count != 0:
            raise Exception(f"Wrapper count not reset. Current: {request.user.profile.wrapper_count}")
        if request.user.profile.bins_emptied <= initial_bins_emptied:
            raise Exception(f"Bins emptied not increased. Before: {initial_bins_emptied}, After: {request.user.profile.bins_emptied}")

        # Process the result of the gym battle
        if did_win == 'true':
            with transaction.atomic():
                #Increase the win count in the user's profile
                increase_win_count(request.user)
                check_and_award_achievements(request.user, 'BATTLES')
                player_collection_cards = get_player_deck(request.user)
                # Reset the gym player's cards from in use to not in use before updating the gym's cards
                reset_gym_player_cards(gym)
                # Set the gym's cards & update the player's cards in use
                update_gym_cards(request.user,player_collection_cards, gym)
                # Clear the cards used by the player in the battle from their deck
                request.user.profile.deck_card_1 = None
                request.user.profile.deck_card_2 = None
                request.user.profile.deck_card_3 = None
                request.user.profile.save() 
                # Update the owning player
                update_owning_player(request.user,gym)
                # Update the cooldown of the gym
                update_cooldown(gym)
                # Add a pack to the user's profile
                add_players_pack(request.user)


        # Check if the user has reached an achievement milestone
        # Increment use count for each card used in the battle and check if any cards have reached max uses
        for card in player_deck_cards:
            player_card = PlayerCards.objects.get(player=request.user, card=card)
            player_card.increment_use()

        battle_cards = []
        for card in player_deck_cards:
            player_card = PlayerCards.objects.get(player=request.user, card=card)
            max_uses = player_card.get_use_count()
            exceeded = player_card.use_count >= max_uses
            battle_cards.append({
            'image_url': card.image.url,
            'exceeded': exceeded,
            })

        context['battle_cards'] = battle_cards
        context['any_expired'] = any(card['exceeded'] for card in context['battle_cards'])

        # Get the players cards and filter out the cards that have reached max uses
        players_cards = PlayerCards.objects.filter(player=request.user)
        # Check and remove cards that have reached max uses
        for player_card in players_cards:
            player_card.check_and_remove()

        return render(request, 'backend/battles/gym-battle-completed.html', context)

@login_required
def gym_not_found(request):
    '''
    Endpoint for when a gym is not found
    '''
    return render(request, 'backend/battles/gym-not-found.html')

@login_required
def missing_battle_condition(request):
    '''
    Endpoint for when a gym battle condition is missing
    '''
    return render(request, 'backend/battles/missing-condition.html')

@login_required
def user_has_no_deck(request):
    '''
    Endpoint for when a user has no deck
    '''
    return render(request, 'backend/battles/no-deck.html')

@login_required
def get_gym_locations(request):
    gyms = Gym.objects.all()
    gym_data = [{"name": gym.name, "latitude": gym.latitude, "longitude": gym.longitude} for gym in gyms]
    return JsonResponse(gym_data, safe=False)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

@login_required
def team_leaderboard(request):
    """Renders template for the team leaderboard"""

    # Get teams that users can select
    teams = Team.objects.filter(user_selectable=True)

    teams_data = []
    for team in teams:
        # Filter gyms owned by players whose profile has this team
        gyms = Gym.objects.filter(owning_player__profile__team_name=team)
        gyms_owned = gyms.count()

        recycle_cards_in_use = 0
        plant_cards_in_use = 0
        plastic_cards_in_use = 0

        # Iterate through each gym to check the cards used in that gym
        for gym in gyms:
            for card in (gym.card1, gym.card2, gym.card3):
                if card.card_type == 2:
                    recycle_cards_in_use += 1
                elif card.card_type == 3:
                    plant_cards_in_use += 1
                elif card.card_type == 1:
                    plastic_cards_in_use += 1

        teams_data.append({
            'icon_url': team.icon.url,
            'name': team.name,
            'currently_owned_gyms': gyms_owned,
            'recycle_cards_in_use': recycle_cards_in_use,
            'plant_cards_in_use': plant_cards_in_use,
            'plastic_cards_in_use': plastic_cards_in_use,
        })

    context = {
        'teams': teams_data,
    }
    return render(request, 'backend/leaderboard/team_leaderboard.html', context)

@login_required
def player_leaderboard(request):
    """
    Renders the Player Leaderboard, excluding any players whose team is 'Fossil Fuels'.
    Shows the top 10 players ordered by the number of gyms they own (descending).
    """

    # Exclude any profiles whose team_name is "Fossil Fuels"
    profiles = Profile.objects.select_related('user', 'team_name') \
                              .exclude(team_name__name="Fossil Fuels")

    players_data = []

    for profile in profiles:
        user = profile.user
        username = user.username
        team = profile.team_name.name  # e.g. "Recycle", "Reuse", etc.

        # Count how many gyms this user owns
        owning_gyms = Gym.objects.filter(owning_player=user).count()

        # Gather all PlayerCards for this user
        player_cards = PlayerCards.objects.filter(player=user)

        # Count cards by type (adjust card_type values if your logic differs)
        plastic_cards_owned = player_cards.filter(card__card_type=3).count()
        recycle_cards_owned = player_cards.filter(card__card_type=1).count()
        plant_cards_owned = player_cards.filter(card__card_type=2).count()

        # Collection total could be the sum of these counts
        collection_total = plastic_cards_owned + recycle_cards_owned + plant_cards_owned

        battles_won = profile.battles_won
        bins_emptied = profile.bins_emptied
        packs_opened = profile.packs_opened

        players_data.append({
            'username': username,
            'team_name': team,
            'owning_gyms': owning_gyms,
            'plastic_cards_owned': plastic_cards_owned,
            'recycle_cards_owned': recycle_cards_owned,
            'plant_cards_owned': plant_cards_owned,
            'collection_total': collection_total,
            'battles_won': battles_won,
            'bins_emptied': bins_emptied,
            'packs_opened': packs_opened,
        })

    # Sort the list in descending order by owning_gyms
    players_data.sort(key=lambda p: p['owning_gyms'], reverse=True)

    # Take the top 10 players
    players_data = players_data[:10]

    context = {
        'players': players_data,
    }

    return render(request, 'backend/leaderboard/player_leaderboard.html', context)
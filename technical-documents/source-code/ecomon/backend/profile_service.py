from accounts.player_service import add_players_pack

def check_achievements(user):
    """Check and award achievements based on user stats"""
    profile = user.profile

    # Store previous stats to check for new achievements
    previous_stats = {
        'packs_opened': profile.packs_opened,
        'battles_won': profile.battles_won,
        'bins_emptied': profile.bins_emptied
    }

    # Check pack opening achievements
    if profile.packs_opened >= 10 and previous_stats['packs_opened'] < 10:
        add_players_pack(user)

    if profile.packs_opened >= 25 and previous_stats['packs_opened'] < 25:
        add_players_pack(user)

    if profile.packs_opened >= 50 and previous_stats['packs_opened'] < 25:
        add_players_pack(user)
    
    # Check battle achievements
    if profile.battles_won >= 10 and previous_stats['battles_won'] < 5:
        add_players_pack(user)

    if profile.battles_won >= 25 and previous_stats['battles_won'] < 25:
        add_players_pack(user)

    if profile.battles_won >= 50 and previous_stats['battles_won'] < 50:
        add_players_pack(user)

    if profile.bins_emptied >= 10 and previous_stats['bins_emptied'] < 10:
        add_players_pack(user)   

    if profile.bins_emptied >= 25 and previous_stats['bins_emptied'] < 25:
        add_players_pack(user)
    
    if profile.bins_emptied >= 50 and previous_stats['bins_emptied'] < 50:
        add_players_pack(user)
    
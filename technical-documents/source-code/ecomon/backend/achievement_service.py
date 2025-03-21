from django.contrib.auth.models import User
from django.db import transaction
from .models import Achievement, PlayerAchievements
from accounts.player_service import add_players_pack
from accounts.models import Profile

@transaction.atomic
def check_and_award_achievements(user:User, stat_type):
    """
    Check and award achievements for a specific stat type
    stat_type should be 'PACKS', 'BATTLES', or 'BINS'
    """

    if stat_type not in ['PACKS', 'BATTLES', 'BINS']:
        raise ValueError("Invalid stat type")
    profile = Profile.objects.get(user=user)
    stat_value = {
        'PACKS': profile.packs_opened,
        'BATTLES': profile.battles_won,
        'BINS': profile.bins_emptied
    }[stat_type]

    # Get achievements that the user qualifies for but hasn't earned yet
    potential_achievements = Achievement.objects.filter(
        type=stat_type,
        threshold__lte=stat_value
    ).exclude(
        playerachievements__player=user
    )

    # Award achievements and packs
    awarded_pack = False
    for achievement in potential_achievements:
        PlayerAchievements.objects.create(
            player=user,
            achievement=achievement,
            pack_awarded=True
        )
        awarded_pack = True
        print(f"Awarded {achievement.name} to {user.username}")

    if awarded_pack:
        add_players_pack(user)
        print(f"Awarded pack to {user.username} for new achievement")

    return awarded_pack

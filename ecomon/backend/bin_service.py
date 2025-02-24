from accounts.models import Profile

MAX_WRAPPER_COUNT = 3

def get_player_wrapper_count(user) -> int:
    '''
    Get the number of wrappers the player has

    Returns the number of wrappers the player has
    '''
    profile = Profile.objects.get(user=user)
    return profile.wrapper_count

def is_bin_full(user) -> bool:
    '''
    Check if the user's bin is full

    Returns True if the user's bin is full
    '''
    return get_player_wrapper_count(user) >= MAX_WRAPPER_COUNT

def increment_wrapper_count(user) -> None:
    '''
    Increment the player's wrapper count
    '''
    profile = Profile.objects.get(user=user)
    profile.wrapper_count += 1
    profile.save()
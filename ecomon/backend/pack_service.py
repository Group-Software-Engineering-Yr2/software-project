'''
Service for pack related operations
'''
from accounts.models import Profile

def get_pack_count(user):
    '''
    Based on the user, return the number of packs they have

    Returns the number of packs a user has
    '''
    profile = Profile.objects.get(user=user)
    return profile.pack_count

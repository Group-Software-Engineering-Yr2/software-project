from django.db import models
from django.contrib.auth.models import User
from backend.models import Team, Card

# Create your models here.


class Profile(models.Model):
    '''
    Weak entity Profile database model extending User 
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    deck_card_1 = models.ForeignKey(Card, on_delete=models.CASCADE,
                                    related_name='profile_deck_card1',
                                    null=True)
    deck_card_2 = models.ForeignKey(Card, on_delete=models.CASCADE,
                                    related_name='profile_deck_card2',
                                    null=True)
    deck_card_3 = models.ForeignKey(Card, on_delete=models.CASCADE,
                                    related_name='profile_deck_card3',
                                    null=True)
    wrapper_count = models.IntegerField()
    pack_count = models.IntegerField()

    # Stats for achievements
    battles_won = models.IntegerField(default=0)
    bins_emptied = models.IntegerField(default=0)
    packs_opened = models.IntegerField(default=0) 



    def __str__(self):
        # Ignore python warning
        return f"{self.user.username}'s Profile"
'''Defining models for the dabase'''
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    '''
    Team database model
    '''
    name = models.CharField(max_length=100,primary_key=True)
    color = models.CharField(max_length=100)
    icon = models.ImageField()

class Card(models.Model):
    '''
    Card database model
    '''
    name = models.CharField(max_length=100, primary_key=True)
    image = models.ImageField()
    card_type = models.IntegerField()
    ability_name_1 = models.CharField(max_length=100)
    ability_power_1 = models.IntegerField()
    ability_name_2 = models.CharField(max_length=100)
    ability_power_2 = models.IntegerField()
    health_points = models.IntegerField()
    fact = models.CharField(max_length=100)

class Gym(models.Model):
    '''
    Gym database model
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    fact = models.CharField(max_length=100)
    # 3 foreign keys to cards
    card1 = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='gym_card1')
    card2 = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='gym_card2')
    card3 = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='gym_card3')
    owning_player = models.ForeignKey(User, on_delete=models.CASCADE) # Can get the team from here
    latitude = models.FloatField()
    longitude = models.FloatField()
    cooldown = models.DateTimeField()



class Profile(models.Model):
    '''
    Weak entity Profile database model extending User 
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    deck_card_1 = models.ForeignKey(Card, on_delete=models.CASCADE,
                                    related_name='profile_deck_card1')
    deck_card_2 = models.ForeignKey(Card, on_delete=models.CASCADE,
                                    related_name='profile_deck_card2')
    deck_card_3 = models.ForeignKey(Card, on_delete=models.CASCADE,
                                    related_name='profile_deck_card3')
    wrapper_count = models.IntegerField()
    pack_count = models.IntegerField()

    def __str__(self):
        # Ignore python warning
        return f"{self.user.username}'s Profile"


class PlayerCards(models.Model):
    '''
    PlayerCards database model
    '''
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    in_gym = models.BooleanField()
    use_count = models.IntegerField() # Depends on the card type, check if this record is removed

class Achievement(models.Model):
    '''
    Achievement database model
    '''
    name = models.CharField(max_length=100, primary_key=True)
    tier = models.IntegerField()
    icon = models.ImageField()

class PlayerAchievements(models.Model):
    '''
    PlayerAchievements database model
    '''
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_unlocked = models.DateTimeField()

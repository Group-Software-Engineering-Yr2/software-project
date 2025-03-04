'''Defining models for the dabase'''
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Team(models.Model):
    '''
    Team database model
    '''
    name = models.CharField(max_length=100,primary_key=True)
    color = models.CharField(max_length=100)
    icon = models.ImageField()
    icon = models.ImageField(upload_to='static/images/teams/')
    user_selectable = models.BooleanField(default=True) # If the user can join this team or not

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
    ability_self_power_2 = models.IntegerField(default=0) 
    health_points = models.IntegerField()
    fact = models.CharField(max_length=200)

    def to_json(self):
        '''Return the card as a json object'''
        return {
            'name': self.name,
            'image': self.image.url,
            'card_type': self.card_type,
            'ability_name_1': self.ability_name_1,
            'ability_power_1': self.ability_power_1,
            'ability_name_2': self.ability_name_2,
            'ability_power_2': self.ability_power_2,
            'ability_self_power_2': self.ability_self_power_2,
            'health_points': self.health_points,
            'fact': self.fact
        }

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
    ACHIEVEMENT_TYPES = [
        ('PACKS', 'Packs Opened'),
        ('BATTLES', 'Battles Won'),
        ('BINS', 'Bins Emptied')
    ]

    ICON_CHOICES = [
        ("static/images/backend/profile/bronzemedal.png", "Bronze"),
        ("static/images/backend/profile/silvermedal.png", "Silver"),
        ("static/images/backend/profile/goldmedal.png", "Gold")
    ]

    name = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES, default='PACKS')
    threshold = models.IntegerField(default = 0)  # e.g., 10, 25, 50
    tier = models.IntegerField(default = 1)  # e.g., 1, 2, 3
    icon = models.CharField(max_length=255, choices=ICON_CHOICES, default="achievements/bronze.png")

class PlayerAchievements(models.Model):
    '''
    PlayerAchievements database model
    '''
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(
        Achievement, 
        on_delete=models.CASCADE,
        null=True,  # Allow null temporarily for migration
        default=None
    )
    date_achieved = models.DateTimeField(default=timezone.now)
    pack_awarded = models.BooleanField(default=False)



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

    def get_use_count(self):
        '''
        Get the maximum number of uses for the card
        '''
        base_max_uses = {
            1: 8, #Plastic cards
            2: 5, #Recycling cards
            3: 3 #Plant cards

        }

        player_team = self.player.profile.team_name.name.lower()
        card_type = self.card.card_type

        max_uses = base_max_uses[card_type]

        if (player_team == 'reuse'): 
            max_uses += 3

        return max_uses


    def check_and_remove(self):
        '''
        Check if the card is to be removed
        '''

        max_allowed = self.get_use_count()

        if self.use_count >= max_allowed:
            self.delete()
            return True
        return False
    
    def increment_use(self):
        """Increment use count and check if card should be deleted"""
        self.use_count += 1
        self.save()
        return self.check_and_delete()



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



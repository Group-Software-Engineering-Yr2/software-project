from rest_framework import serializers
from .models import Team, Card, Gym, PlayerCards, Achievement, PlayerAchievements

class TeamSerializer(serializers.ModelSerializer):
    '''Team Serializer'''
    class Meta:
        '''Meta class'''
        model = Team
        fields = ['name', 'color', 'icon']


class CardSerializer(serializers.ModelSerializer):
    '''Card Serializer'''
    class Meta:
        '''Meta class'''
        model = Card
        fields = [
            'name', 'image', 'card_type', 'ability_name_1', 'ability_power_1',
            'ability_name_2', 'ability_power_2','ability_self_power_2' 'health_points', 'fact'
        ]


class GymSerializer(serializers.ModelSerializer):
    '''Gym Serializer'''
    card1 = CardSerializer(read_only=True)
    card2 = CardSerializer(read_only=True)
    card3 = CardSerializer(read_only=True)
    owning_player = serializers.StringRelatedField()  # Returns username instead of ID

    class Meta:
        '''Meta class'''
        model = Gym
        fields = [
            'id', 'name', 'fact', 'card1', 'card2', 'card3',
            'owning_player', 'latitude', 'longitude', 'cooldown'
        ]


class PlayerCardsSerializer(serializers.ModelSerializer):
    '''PlayerCards Serializer'''
    player = serializers.StringRelatedField()  # Returns username instead of ID
    card = CardSerializer(read_only=True)

    class Meta:
        '''Meta class'''
        model = PlayerCards
        fields = ['player', 'card', 'in_gym', 'use_count']


class AchievementSerializer(serializers.ModelSerializer):
    '''Achievement Serializer'''
    class Meta:
        '''Meta class'''
        model = Achievement
        fields = ['ACHIEVEMENT_TYPES','ICON_CHOICES', 'name', 'type', 'threshold', 'tier', 'icon']

    
class PlayerAchievementsSerializer(serializers.ModelSerializer):
    '''PlayerAchievements Serializer'''
    player = serializers.StringRelatedField()  # Returns username instead of ID
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        '''Meta class'''
        model = PlayerAchievements
        fields = [
            'player', 'achievement', 'date_achieved', 'pack_awarded'
        ]


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from backend.serializers import TeamSerializer, CardSerializer
from backend.models import Team
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    '''Profile Serializer'''
    user = serializers.StringRelatedField()  # Returns the username instead of the ID
    team = TeamSerializer(source='team_id', read_only=True)
    deck_card_1 = CardSerializer(read_only=True)
    deck_card_2 = CardSerializer(read_only=True)
    deck_card_3 = CardSerializer(read_only=True)

    class Meta:
        '''Meta class'''
        model = Profile
        fields = [
            'user', 'team', 'deck_card_1', 'deck_card_2', 'deck_card_3',
            'wrapper_count', 'pack_count'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    '''Serializer for registering a new user'''
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    team_name = serializers.CharField(write_only=True)

    class Meta:
        '''Meta class'''
        model = User
        fields = ['username', 'email', 'password','team_name']

    def create(self, validated_data):
        '''Create a new user'''

        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )

            team = Team.objects.filter(name=validated_data['team_name']).first()

            Profile.objects.create(
                user=user,
                team_name = team,
                wrapper_count = 0,
                pack_count = 0
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))

class LoginSerializer(serializers.Serializer):
    '''Serializer for user login'''
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        '''Authenticate user'''
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        # Get or create auth token for the user
        token, created = Token.objects.get_or_create(user=user)

        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token.key,
        }

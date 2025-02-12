from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer, LoginSerializer


class UserProfileView(APIView):
    '''
    Rest API view for user profile
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''Get user profile'''
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateProfileView(APIView):
    '''Update profile REST API'''
    permission_classes = [IsAuthenticated]

    def put(self, request):
        '''Update user profile'''
        try:
            profile = Profile.objects.get(user=request.user)
            data = request.data

            # Update only the fields that are provided
            profile.wrapper_count = data.get("wrapper_count", profile.wrapper_count)
            profile.pack_count = data.get("pack_count", profile.pack_count)

            # If new cards are provided, update them
            if "deck_card_1" in data:
                profile.deck_card_1_id = data["deck_card_1"]
            if "deck_card_2" in data:
                profile.deck_card_2_id = data["deck_card_2"]
            if "deck_card_3" in data:
                profile.deck_card_3_id = data["deck_card_3"]
            if "team_id" in data:
                profile.team_id_id = data["team_id"]

            profile.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    '''Register a new user REST API'''
    def post(self, request):
        '''Register a new user'''
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    '''Login a user and return a token'''
    def post(self, request):
        '''Authenticate user'''
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

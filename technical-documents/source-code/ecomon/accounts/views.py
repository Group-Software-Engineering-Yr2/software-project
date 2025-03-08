from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Profile, Team
from .serializers import ProfileSerializer, RegisterSerializer, LoginSerializer
from .forms import CustomUserCreationForm

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

def render_sign_up(request):
    '''Render sign-up page and handle user registration'''
    teams = Team.objects.filter(user_selectable=True)

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "Account created successfully!")
            return redirect("/home")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/sign-up.html", {"teams": teams, "form": form})

def render_login(request):
    '''Render login page and authenticate users using email and password'''
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Get user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, "accounts/login.html")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"")
            return redirect("/home")  # Redirect to homepage
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")

def render_privacy(request):
    return render(request, "accounts/privacy.html")

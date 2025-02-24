from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Team

class CustomUserCreationForm(UserCreationForm):
    '''Creating Ecomon User'''
    email = forms.EmailField(required=True)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=True)

    class Meta:
        '''Data fields for User'''
        model = User
        fields = ["username", "email", "password1", "password2", "team"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            team = self.cleaned_data["team"]
            Profile.objects.create(
                user=user,
                team_name=team,
                wrapper_count=0,
                pack_count=1
            )
        return user

class CustomAuthenticationForm(forms.Form):
    '''Custom authentication form to allow login via email'''
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}), required=True
    )

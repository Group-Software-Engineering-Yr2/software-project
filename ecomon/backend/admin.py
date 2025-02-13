from django.contrib import admin

# Register your models here.


from .models import Team, Card, Gym, PlayerCards, Achievement, PlayerAchievements

admin.site.register(Team)
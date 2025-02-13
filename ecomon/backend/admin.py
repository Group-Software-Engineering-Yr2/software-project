from django.contrib import admin

# Register your models here.


from .models import Team, Card, Gym, PlayerCards, Achievement, PlayerAchievements

admin.site.register(Team)
admin.site.register(Card)
admin.site.register(Gym)
admin.site.register(PlayerAchievements)
admin.site.register(PlayerCards)
admin.site.register(Achievement)


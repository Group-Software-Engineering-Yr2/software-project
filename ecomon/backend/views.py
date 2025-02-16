from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here

# @login_required
def render_scanner(request):
    return render(request, 'backend/scanner.html')

# @login_required
def render_gym_battle(request, gym_id):
    return render(request, "backend/gym_battle.html", {"gym_id": gym_id})

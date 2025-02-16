from django.http import HttpResponse
from django.shortcuts import render

# Create your views here


def example_view(request):
    return HttpResponse('Hello, World!')


def profile(request):
    return render(request, 'profile/profile.html')
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here


def example_view(request):
    return HttpResponse('Hello, World!')

def index(request):
    '''Redirects user based on authentication status'''
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/accounts/register')

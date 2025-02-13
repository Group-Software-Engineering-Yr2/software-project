from django.http import HttpResponse

# Create your views here


def example_view(request):
    return HttpResponse('Hello, World!')
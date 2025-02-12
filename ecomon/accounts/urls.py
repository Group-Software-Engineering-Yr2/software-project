from django.urls import path
from .views import UserProfileView, UpdateProfileView, RegisterView, LoginView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/update/', UpdateProfileView.as_view(), name='update-profile'),
]

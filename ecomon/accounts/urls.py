from django.urls import path
from .views import UserProfileView, UpdateProfileView, RegisterView, LoginView, render_sign_up, render_login

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('register/', render_sign_up, name='register-page'),
    path('login/', render_login, name='login-page'),
]

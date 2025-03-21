from django.urls import path
from .views import UserProfileView, UpdateProfileView, RegisterView, LoginView, render_privacy, render_sign_up, render_login, UpdateEmailView, UpdatePasswordView, UpdateUsernameView, DeleteAccountView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('api/profile/update/username/', UpdateUsernameView.as_view(), name='update-username'),
    path('api/profile/update/email/', UpdateEmailView.as_view(), name='update-email'),
    path('api/profile/update/password/', UpdatePasswordView.as_view(), name='update-password'),
        path('api/profile/delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('register/', render_sign_up, name='register-page'),
    path('login/', render_login, name='login-page'),
    path('privacy/', render_privacy, name='privacy')
]

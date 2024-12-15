from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, ResetPassword, UserUpdateView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('reset_password', ResetPassword.as_view(), name='reset_password'),
    path('user_update/', UserUpdateView.as_view(template_name='profile_form.html'), name='user_update'),
    path('login/profile/', UserDetailView.as_view(template_name='profile.html'), name='profile'),
]
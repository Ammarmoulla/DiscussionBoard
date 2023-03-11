from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="accounts/change_password.html"), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="accounts/change_password_done.html"), name="password_change_done"),
]
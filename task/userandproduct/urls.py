from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, login, logout, dashboard, mainpage

urlpatterns = [
    path("", dashboard, name="home"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("user_mainpage/", mainpage, name="mainpage"),
]
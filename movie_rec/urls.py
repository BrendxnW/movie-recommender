from django.urls import path
from .import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("recommender/", views.recommender, name="recommender"),
    path("remixer/", views.remixer, name="remixer"),
]
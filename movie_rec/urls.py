from django.urls import path
from .import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("greet/", views.greet_view, name="greet"),
    path('search-movies/', views.search_movies, name='search_movies'),
]
from django.urls import path
from .import views

urlpatterns = [
    path("", views.greet_view),
    path("greet/", views.greet_view, name="greet"),
    path('search-movies/', views.search_movies, name='search_movies'),
]
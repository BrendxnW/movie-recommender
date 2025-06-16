import requests
import random
from config import *


class InvalidGenreError(Exception):
    """
    Custom error if there is an invalid genre
    """
    pass


def get_movie_genre_id(genre_name):
    """
    Gets the movie id from the given genre
    """
    url = f"{BASE_URL}/genre/movie/list?language=en"

    headers = HEADERS
    response = requests.get(url, headers=headers)

    genres = response.json().get("genres", [])
    for genre in genres:
        if genre["name"].title() == genre_name.title():
            return genre["id"]
    raise InvalidGenreError(f"Unfamiliar with the genre: \"{genre_name}\"")


def get_movies_by_genre(genre_name):
    """
    Gets movies by genre
    """
    genre_id = get_movie_genre_id(genre_name.title())

    url = f"{BASE_URL}/discover/movie?with_genres={genre_id}&include_adult=true&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

    headers = HEADERS
    response = requests.get(url, headers=headers)

    data = response.json()
    titles = [movie["title"] for movie in data.get("results", [])]
    return random.sample(titles, k=(5))


def get_movies_with_actors(actor_name):
    """
    Gets movie recommendation with the actor in the movie
    """


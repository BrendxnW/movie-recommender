import os
from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


class InvalidGenreError(Exception):
    """
    Custom Error if there is an invalid genre
    """
    pass

def get_movie_genre_id(genre_name):
    """
    Gets the movie id from the given genre
    """
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    genres = response.json().get("genres", [])
    for genre in genres:
        if genre["name"].lower() == genre_name.lower():
            return genre["id"]
    raise InvalidGenreError(f"Unfamiliar with the genre: \"{genre_name}\"")


def get_movies_by_genre(genre):
    """
    Gets movies by genre
    """
    genre_id = get_movie_genre_id(genre.lower())

    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.text

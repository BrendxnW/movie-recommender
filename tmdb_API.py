import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMDhiN2ZmNTIzMWMyNTE3YzQ3YjEyZmM5NTk3YTFiYyIsIm5iZiI6MTc0ODU2NzMyMy42MzUsInN1YiI6IjY4MzkwNTFiYzdkMWEzYjgyOTA4MDdlZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BeX-zrb02dndbiIdfly0cNqeRlA6gtG0rUjvuHhEJC8"


def get_movie_genre_id():
    """
    Gets the movie genere id
    """
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    genres = response.json().get("genres", [])
    return {genre["names"].lower() : genre["id"] for genre in genres}
    

def get_movies_by_genere(genre):
    """
    Gets movies by genere
    """
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.text


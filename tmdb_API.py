import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

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


import requests
import random
from django.conf import settings


class InvalidGenreError(Exception):
    """
    Custom error if there is an invalid genre
    """
    pass

class InvalidActorError(Exception):
    """
    Custom error if there is an invalid actor name
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
        if genre["name"].title().strip() == genre_name.title().strip():
            return genre["id"]
    raise InvalidGenreError(f"Unfamiliar with the genre: \"{genre_name}\"")


def get_movies_by_genre(genre_name):
    """
    Gets movies recommendation with genre
    """
    genre_id = get_movie_genre_id(genre_name.title())

    url = f"{BASE_URL}/discover/movie"
    headers = HEADERS

    for _ in range(5):
        params = {
            "with_genres": genre_id,
            "include_adult": False,
            "include_video": False,
            "language": "en-US",
            "page": random.randint(1, 20),
            "vote_average.gte": 6.5,
            "vote_count.gte": 100
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        titles = [movie["title"] for movie in data.get("results", [])]
        if len(titles) >= 5:
            random.shuffle(titles)
            return titles[:5]
    return ["No recommendations found."]


def get_movies_by_actors(actor_name):
    """
    Gets movie recommendation with the actor in the movie
    """
    url = f"{BASE_URL}/discover/movie?with_cast={actor_name}&include_adult=true&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    headers = HEADERS

    for _ in range(5):
        if actor_name != with_cast:
            raise InvalidActorError(f"Can't find the actor: {actor_name.title()}")
        params = {
            "with_cast": actor_name.title(),
            "include_adult": False,
            "include_video": False,
            "language": "en-US",
            "page": random.randint(1, 20),
            "vote_average.gte": 6.5,
            "vote_count.gte": 100
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        titles = [movie["title"] for movie in data.get("results", [])]
        if len(titles) >= 3:
            random.shuffle(titles)
            return titles[:3]
    return ["No recommendations found."]
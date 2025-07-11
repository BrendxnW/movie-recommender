import requests
import random
from django.conf import settings

class InvalidGenreError(Exception):
    """Custom error if there is an invalid genre"""
    pass

class InvalidActorError(Exception):
    """Custom error if there is an invalid actor name"""
    pass


def get_movie_genre_id(genre_name):
    """
    Gets the movie id from the given genre.
    Expects a cleaned genre name (e.g., 'comedy', 'horror', 'science fiction').
    """
    url = f"{settings.BASE_URL}/genre/movie/list?language=en"
    headers = settings.HEADERS
    response = requests.get(url, headers=headers)
    genres = response.json().get("genres", [])

    genre_name_clean = genre_name.lower().strip()
    for genre in genres:
        if genre["name"].lower().strip() == genre_name_clean:
            return genre["id"]
    available = ", ".join([g["name"] for g in genres])
    raise InvalidGenreError(f"Unfamiliar with the genre: \"{genre_name}\". Available genres: {available}")


def get_movies_by_genre(genre_name):
    """
    Gets movie recommendations for a genre.
    Expects a cleaned genre name.
    """
    genre_id = get_movie_genre_id(genre_name)

    url = f"{settings.BASE_URL}/discover/movie"
    headers = settings.HEADERS

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
        movies = data.get("results", [])

        if len(movies) >= 5:
            random.shuffle(movies)
            return [
                {
                    "title": movie["title"],
                    "description": movie.get("overview", "No description available.")
                }
                for movie in movies[:5]
            ]
    return ["No recommendations found."]


import requests
import random
from django.conf import settings
from local_data import keyword_to_movies, movie_id_to_info


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


def get_movie_trailer(movie_id):
    """
    Gets the movie trailer from YouTube
    """
    url = f"{settings.BASE_URL}/movie/{movie_id}/videos"
    headers = settings.HEADERS
    params = {"language": "es-US"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        trailer = response.json().get("results", [])

        for video in trailer:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
        return None

    except Exception as e:
        print(f"Error fetching trailer for movie {movie_id}: {e}")
        return None


def get_movies_by_genre(genre_names):
    """
    Gets movie recommendations for a genre.
    Expects a cleaned genre name.
    """
    if isinstance(genre_names, str):
        genre_names = [genre_names]

    all_movies = []

    for genre_name in genre_names:
        try:
            genre_id = get_movie_genre_id(genre_name)
            url = f"{settings.BASE_URL}/discover/movie"
            headers = settings.HEADERS

            for _ in range(3):  # Try 3 pages per genre
                params = {
                    "with_genres": genre_id,
                    "include_adult": False,
                    "include_video": False,
                    "language": "en-US",
                    "page": random.randint(1, 20),
                    "vote_average.gte": 6.5,
                    "vote_count.gte": 100,
                    "primary_release_date.gte": "2005-01-01",
                }
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                movies = data.get("results", [])

                if movies:
                    all_movies.extend(movies)
                    break
        except InvalidGenreError:
            continue

    # Remove duplicates and return top 5
    unique_movies = []
    seen_titles = set()

    for movie in all_movies:
        if movie["title"] not in seen_titles:
            seen_titles.add(movie["title"])
            unique_movies.append(movie)

    if len(unique_movies) >= 5:
        random.shuffle(unique_movies)
        movie_dicts = []
        for movie in unique_movies[:5]:
            trailer_url = get_movie_trailer(movie["id"])
            movie_dicts.append({
                "title": movie["title"],
                "description": movie.get("overview", "No description available."),
                "trailer_url": trailer_url
            })
        return movie_dicts

    return ["No Recommended Movies Available"]


def get_movie_plot(title, api_key=settings.API_KEY):
    url = f"{settings.BASE_URL}/search/movie?api_key={settings.API_KEY}&query={requests.utils.quote(title)}"
    response = requests.get(url)
    data = response.json()
    if data["results"]:
        movie_id = data["results"][0]["id"]
        # Get movie details
        details_url = f"{settings.BASE_URL}/movie/{movie_id}?api_key={api_key}"
        details_response = requests.get(details_url)
        details = details_response.json()
        return details.get("overview", "Plot not found.")
    return "Plot not found."


def search_movies_by_description(keywords):
    matched_movies = set()
    for kw in keywords:
        if kw.lower() in keyword_to_movies:
            matched_movies.update(keyword_to_movies[kw.lower()])
    return [movie_id_to_info[mid] for mid in matched_movies]
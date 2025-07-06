from django.test import TestCase
from .tmdb_API import get_movie_genre_id, get_movies_by_genre, InvalidGenreError

class MovieUtilsTests(TestCase):
    def test_valid_genre_(self):
        genre_id = get_movie_genre_id("Comedy")
        self.assertIsInstance(genre_id, int)

    def test_invalid_genre(self):
        with self.assertRaises(InvalidGenreError):
            get_movie_genre_id("NotARealGenre")

    def test_get_movies_by_genre(self):
        movies = get_movies_by_genre("Comedy")
        self.assertIsInstance(movies, list)
        self.assertTrue(all(isinstance(title, str) for title in movies))
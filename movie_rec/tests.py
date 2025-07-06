from django.test import TestCase
from .tmdb_API import get_movie_genre_id, get_movies_by_genre, InvalidGenreError

class MovieUtilsTests(TestCase):
    def test_valid_genre_(self):
        genre_id = get_movie_genre_id("Comedy")
        self.assertIsInstance(genre_id, int)
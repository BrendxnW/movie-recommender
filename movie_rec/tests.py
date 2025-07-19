from django.test import TestCase
from .tmdb_API import get_movie_genre_id, get_movies_by_genre, InvalidGenreError
from .nlp_utils import Remixer

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

    def test_remixer(self):
        plot1 = "A young aristocratic woman falls in love with a free-spirited artist aboard the ill-fated maiden voyage of the RMS Titanic. As their romance blossoms, the looming iceberg collision threatens their future and tests the power of love and survival."
        plot2 = "A computer hacker named Neo discovers that reality as he knows it is a simulation controlled by intelligent machines. After being freed from the virtual illusion, he joins a rebellion to fight against the machine overlords and uncover the truth about human existence."

        r = Remixer()

        # Generate multiple variations
        print("🎬 Multiple Remixed Plots:\n")
        for i in range(3):
            remix = r.plot_mixer(plot1, plot2)
            print(f"Version {i + 1}:\n{remix}\n")

class MovieUtilsTests(TestCase):
    def test_valid_genre(self):
        genre_id = get_movie_genre_id("Comedy")
        self.assertIsInstance(genre_id, int)

    def test_invalid_genre(self):
        with self.assertRaises(InvalidGenreError):
            get_movie_genre_id("NotARealGenre")

    def test_get_movies_by_genre(self):
        movies = get_movies_by_genre("Comedy")
        self.assertIsInstance(movies, list)
        self.assertTrue(all(isinstance(movie, dict) for movie in movies))
        self.assertTrue(all("title" in movie for movie in movies))

    def test_remixer(self):
        plot1 = "A young aristocratic woman falls in love with a free-spirited artist aboard the ill-fated maiden voyage of the RMS Titanic. As their romance blossoms, the looming iceberg collision threatens their future and tests the power of love and survival."
        plot2 = "A computer hacker named Neo discovers that reality as he knows it is a simulation controlled by intelligent machines. After being freed from the virtual illusion, he joins a rebellion to fight against the machine overlords and uncover the truth about human existence."

        r = Remixer()
        remix = r.plot_mixer(plot1, plot2)
        self.assertIsInstance(remix, str)
        self.assertTrue(len(remix) > 0)

    def test_remixer_no_vibe(self):
        plot1 = (
            "Dom Cobb (Leonardo DiCaprio) is a thief with the rare ability to enter people's dreams and steal their secrets from their subconscious. "
            "His skill has made him a hot commodity in the world of corporate espionage but has also cost him everything he loves. "
            "Cobb gets a chance at redemption when he is offered a seemingly impossible task: Plant an idea in someone's mind. "
            "If he succeeds, it will be the perfect crime, but a dangerous enemy anticipates Cobb's every move."
        )
        plot2 = (
            "the formation of the superhero team to combat Loki and his alien army, the Chitauri, who are attempting to conquer Earth. "
            "Loki, using the Tesseract and his scepter, manipulates several S.H.I.E.L.D. agents, including Hawkeye and Dr. Selvig, to aid his invasion. "
            "Iron Man, Captain America, Thor, the Hulk, Black Widow, and Hawkeye are brought together by Nick Fury, director of S.H.I.E.L.D., to fight back. "
            "The team faces internal conflicts and must learn to work together to stop Loki's invasion and close the portal opened by the Tesseract. "
            "Ultimately, they succeed in defeating Loki and the Chitauri, saving New York City and the world."
        )
        result = Remixer().plot_mixer(plot1, plot2)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_remixer_one_vibe(self):
        plot1 = "Dom Cobb (Leonardo DiCaprio) is a thief with the rare ability to enter people's dreams and steal their secrets from their subconscious."
        plot2 = "The Avengers assemble to save the world from Loki and his alien army."
        result = Remixer().plot_mixer(plot1, plot2, vibes=["funny"])
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_remixer_two_vibes(self):
        plot1 = "Dom Cobb (Leonardo DiCaprio) is a thief with the rare ability to enter people's dreams and steal their secrets from their subconscious."
        plot2 = "The Avengers assemble to save the world from Loki and his alien army."
        result = Remixer().plot_mixer(plot1, plot2, vibes=["funny", "dark"])
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
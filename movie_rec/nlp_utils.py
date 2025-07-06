from transformers import pipeline
import torch
import random
import re


device = torch.device('cpu')


class GreetingPrompt:
    """
    Testing another version of greeting prompt
    """

    def __init__(self, name):
        self.name = name

    def generate_prompt(self):
        hellos = ['Hi,', 'Hello,', 'Howdy,', 'Hey there,', 'Heyo,']
        return f"{random.choice(hellos)} {self.name}!"


class RecommendMovie:
    """
    Classifies movies based on user input.
    """
    def __init__(self):
        self.generator = pipeline("text2text-generation", model="google/flan-t5-base")

    @staticmethod
    def clean_genre_output(genre):
        genre_synonyms = {
            "sci fi": "Science Fiction",
            "scifi": "Science Fiction",
            "romcom": "Romance",
            "cartoon": "Animation",
            "animated": "Animation",
            "action adventure": "Action",
        }
        genre = genre.lower()
        genre = re.sub(r'[^\w\s]', '', genre)  # Remove punctuation
        genre = genre.replace("movie", "").replace("film", "").replace("movies", "").replace("films", "")
        genre = genre.strip()
        genre = ' '.join(genre.split())  # Normalize whitespace
        return genre_synonyms.get(genre, genre.title())

    def classify_genre(self, user_input):
        prompt = (
            "You are a movie recommender bot.\n"
            "Classify the movie genre based on the user's request.\n\n"
            f"User: {user_input}\n"
            "Genre:"
        )

        outputs = self.generator(
            prompt,
            max_new_tokens=50,
            do_sample=True,
            temperature=0.7,
        )

        response = outputs[0]["generated_text"]
        genre_only = response.split("Genre:")[-1].strip()
        genre_cleaned = self.clean_genre_output(genre_only)
        return genre_cleaned


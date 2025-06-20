from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from accelerate import init_empty_weights, infer_auto_device_map
import torch
import random


device = torch.device('cpu')


class GreetingPrompt:
    """
    Testing another version of greeting prompt
    """

    def __init__(self, name):
        self.name = name

    def generate_prompt(self, name):
        hellos = ['Hi,', 'Hello,', 'Howdy,', 'Hey there,', 'Heyo,']
        return (f"{random.choice(hellos)} {self.name}!")


class RecommendMovie:
    """
    """
    def __init__(self):
        self.generator = pipeline("text2text-generation", model="google/flan-t5-base")


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
        return genre_only


    def find_movie(self):
        """
        Finds what type of movie the user is looking for based on their answer
        """
        get_movies = input("What type of movie are you looking for?\n")
        find_genre = self.classify_genre(get_movies)

        return find_genre

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re
from .tmdb_API import *


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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
            "romcom": "Romance, Comedy",
            "rom-com": "Romance, Comedy",
            "romantic comedy": "Romance, Comedy",
            "cartoon": "Animation",
            "animated": "Animation",
            "action adventure": "Action, Adventure",
            "horror comedy": "Horror, Comedy",
            "comedy horror": "Horror, Comedy",
            "drama comedy": "Drama, Comedy",
            "comedy drama": "Drama, Comedy",
            "funny and romantic": "Comedy, Romance",
            "romantic and funny": "Comedy, Romance",
            "scary and funny": "Horror, Comedy",
            "funny and scary": "Horror, Comedy",
        }
        genre = genre.lower()
        genre = re.sub(r'[^\w\s]', '', genre)
        genre = genre.replace("movie", "").replace("film", "").replace("movies", "").replace("films", "")
        genre = genre.strip()
        genre = ' '.join(genre.split())

        raw_list = re.split(r',| and | & ', genre)
        cleaned = []

        for g in raw_list:
            g = g.strip()
            if not g:
                continue

            # Map synonyms or title case
            cleaned_genre = genre_synonyms.get(g, g.title())

            # If synonym returns multiple genres separated by comma, split them
            if ',' in cleaned_genre:
                cleaned.extend([x.strip() for x in cleaned_genre.split(',')])
            else:
                cleaned.append(cleaned_genre)

        # Remove duplicates while preserving order
        seen = set()
        unique_genres = []
        for g in cleaned:
            if g not in seen:
                seen.add(g)
                unique_genres.append(g)

        return unique_genres

    def classify_genre(self, user_input):
        prompt = (
            "You are a movie recommender bot.\n"
            "Classify the movie genre based on the user's request.\n"
            "IMPORTANT: If the user mentions multiple feelings or genres, list ALL of them.\n"
            "Examples:\n"
            "- 'funny and romantic' → Comedy, Romance\n"
            "- 'scary and funny' → Horror, Comedy\n"
            "- 'action and adventure' → Action, Adventure\n"
            "- 'I want something funny and romantic' → Comedy, Romance\n"
            "- 'something scary but also funny' → Horror, Comedy\n"
            "Always separate multiple genres with commas.\n\n"
            f"User: {user_input}\n"
            "Genre:"
        )

        outputs = self.generator(
            prompt,
            max_new_tokens=50,
            do_sample=True,
            temperature=0.8,
        )
        response = outputs[0]["generated_text"]
        genre_only = response.split("Genre:")[-1].strip()
        genre_cleaned = self.clean_genre_output(genre_only)

        return genre_cleaned


class FindMovie:
    """
    Finds a couple movie suggestions
    """
    def __init__(self):
        self.recommender = RecommendMovie()

    def suggest(self, user_input):
        """
        Finds what type of movie the user is looking for based on their answer
        """
        find_genre = self.recommender.classify_genre(user_input)
        return f"Sounds like you're looking for a {find_genre} movie."


class Remixer:
    """
    Remixes two movie plots into one using a creative text generation model.
    """
    AVAILABLE_VIBES = [ "funny", "dark", "romantic", "mysterious", "tragic", "action-packed", "wholesome"]

    @staticmethod
    def get_available_vibes():
        return Remixer.AVAILABLE_VIBES

    def __init__(self):
        # Use a model better suited for creative writing
        model_name = "mosaicml/mpt-7b-storywriter"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if torch.cuda.is_available():
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                load_in_4bit=True,
                device_map="auto"
            )
        else:
            # Fallback to normal float32 on CPU (slower, lots of RAM)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                device_map=None
            )

            # Set pad token if missing
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto" if torch.cuda.is_available() else None
        )


    def plot_mixer(self, plot1, plot2, vibes=None):
        """
        Remixes two movie plots into one unique plot with varied outputs
        """
        vibe_instruction = ""
        if vibes:
            vibe_instruction = "Write the combined story with a " + " and ".join(vibes) + " vibe."

        # Create multiple different prompt variations
        prompts = [
            f"Combine these movie plots into one creative story.{vibe_instruction}\nPlot 1: {plot1}\nPlot 2: {plot2}\nCombined story:",
            f"Merge these two movie plots.{vibe_instruction}\nFirst plot: {plot1}\nSecond plot: {plot2}\nNew story:",
            f"Create a new movie by mixing these plots.{vibe_instruction}\n{plot1}\n{plot2}\nResult:",
            f"Blend these movie plots into one.{vibe_instruction}\nPlot A: {plot1}\nPlot B: {plot2}\nBlended plot:"
        ]

        # Randomly select a prompt
        prompt = random.choice(prompts)

        # Vary the parameters for more diversity
        temperature = random.uniform(0.8, 1.2)
        top_p = random.uniform(0.85, 0.95)

        outputs = self.pipeline(
            prompt,
            max_new_tokens=200,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            top_k=random.randint(30, 70),
            num_return_sequences=1,
            repetition_penalty=random.uniform(1.1, 1.3),
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_text = outputs[0]["generated_text"]

        # Remove the original prompt
        if prompt in generated_text:
            result = generated_text.replace(prompt, "").strip()
        else:
            result = generated_text.strip()

        return result

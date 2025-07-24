from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re
from .tmdb_API import *
import os


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
    AVAILABLE_VIBES = {
        "funny": "comedy of errors and unexpected humor",
        "dark": "descent into darkness and moral ambiguity",
        "romantic": "love story that transcends boundaries",
        "mysterious": "enigmatic puzzle that defies explanation",
        "tragic": "heartbreaking journey of loss and redemption",
        "action-packed": "thrilling adventure with high stakes",
        "wholesome": "heartwarming tale of hope and friendship"
    }

    @staticmethod
    def get_available_vibes():
        return Remixer.AVAILABLE_VIBES

    def __init__(self):
        try:
            model_name = "microsoft/phi-2"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto" if torch.cuda.is_available() else None,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )

            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto" if torch.cuda.is_available() else None,
            )

            print("✅ Model loaded successfully")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("🔄 Falling back to template-based remixer")
            self.model = None
            self.tokenizer = None
            self.pipeline = None

    def plot_mixer(self, plot1, plot2, vibes=None):
        try:
            if not self.pipeline:
                raise ValueError("Model pipeline is not initialized.")

            plot1_clean = self._clean_plot(plot1)
            plot2_clean = self._clean_plot(plot2)

            vibe_instruction = ""
            if vibes:
                vibe_instruction = f" Write the combined story with a {', '.join(vibes)} vibe."

            prompt = (
                f"You are a creative screenwriter. Merge the following two movie plots into one unique and original story:\n\n"
                f"Plot 1: {plot1_clean}\n"
                f"Plot 2: {plot2_clean}\n\n"
                f"Create a new storyline that blends characters, settings, or themes from both. "
                f"Avoid directly copying sentences from the original plots. Surprise the reader with creativity, twists, or emotional depth."
                f"{vibe_instruction}"
            )

            outputs = self.pipeline(
                prompt,
                max_new_tokens=300,
                do_sample=True,
                temperature=0.85,
                top_p=0.92,
                top_k=50,
                num_return_sequences=1,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

            generated_text = outputs[0]["generated_text"]
            result = self._clean_generated_text(generated_text, prompt)

            return result

        except Exception as e:
            print(f"❌ plot_mixer error: {e}")
            return "Sorry, an error occurred while remixing the plot. Please try again later."


    def _clean_plot(self, plot):
        """Smart plot cleaning with better truncation"""
        if not plot or plot == "Plot not found.":
            return "an unknown story"

        plot = plot.replace("Plot not found.", "").strip()

        # If plot is too long, try to find a good breaking point
        if len(plot) > 300:
            # Try to find a complete sentence
            sentences = plot.split('.')
            if len(sentences) > 1:
                # Take first two sentences if they exist
                first_two = '. '.join(sentences[:2]).strip()
                if len(first_two) > 50:
                    return first_two + "."

            # If no good sentence break, take first 300 chars
            if len(plot) > 300:
                return plot[:300].strip()

        return plot if plot else "an unknown story"


    def _clean_generated_text(self, generated_text, prompt):
        # Remove prompt from generated text to get only the generated continuation
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):]
        return generated_text.strip()


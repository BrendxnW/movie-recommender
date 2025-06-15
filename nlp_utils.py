from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import random as ran


class GreetingPrompt:
    """
    Ranomly generates a greeting prompt
    """
    def __init__(self):
        model_name = "ramsrigouthamg/t5_paraphraser"
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.generator = pipeline('text2text-generation', model=model, tokenizer=tokenizer)

    def generate_greeting(self, seed_text="Hello! What is your name?", num_prompts=5, max_length=30):
        input_text = f"paraphrase: {seed_text}"
        outputs = self.generator(
            input_text,
            max_length=max_length,
            num_return_sequences=num_prompts,
            num_beams=max(num_prompts, 5),
            truncation=True
        )
        return [out['generated_text'].strip() for out in outputs]



class GreetingPromptTest:
    """
    Testing another version of greeting prompt
    """

    def __init__(self, name):
        self.name = name

    def generate_prompt(self, name):
        hellos = ['Hi,', 'Hello,', 'Howdy,', 'Hey there,', 'Heyo,']
        return (f"{ran.choice(hellos)} {self.name}!")


class RecommendMovie:
    """
    Finds the recommened types of movies for the user
    """

    def __init__(self):
        model_name = "meta-llama/Llama-3.1-8B"
        pipeline = transformers.pipeline("text-generation", model=model_name, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")

    def find_movie(self):
        """
        Finds what type of movie the user is looking for based on their answer
        """
        get_movies = self.pipeline("What type of movie are you looking for?\n")

        return get_movies
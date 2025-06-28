import numpy as np
import pandas as pd
import torch
from .nlp_utils import GreetingPrompt, RecommendMovie
from .recommender import FindMovie

device = torch.device('cpu')


class ChatBot:
    """
    Creates a chatbot that prompts the user with how they are feeling or what type of movie they are looking for.
    """
    def __init__(self):
        pass


    def greeting(self):
        """
        Greets the user and asks for their name.
        """
        name = input("What can I call you?\n").capitalize()
        greeter = GreetingPrompt(name)
        return greeter.generate_prompt()


    def prompts(self):
        """
        Asks the user with randomized prompts of what type of movie they're looking for.
        """
        
        options = int(input("\nFeatures:\n[1] Movie Recommender\n[2] Movie Remixer\n"))


        if options == 1:
            return FindMovie().suggest()
        if options == 2:
            return "Feature coming soon"
        return None


if __name__ == "__main__":
    
    chat = ChatBot()
    print(chat.greeting())
    input(chat.prompts())
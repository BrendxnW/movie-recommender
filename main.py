import numpy as np
import pandas as pd
import random as ran
import torch
from nlp_utils import GreetingPromptTest

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

        name = input("What can I call you?\n")
        greeter = GreetingPromptTest(name)
        return greeter.generate_prompt(name)


    def prompts(self):
        """
        Asks the user with randomized prompts of what type of movie they're looking for.
        """
        pass


if __name__ == "__main__":
    
    chat = ChatBot()
    print(chat.greeting())
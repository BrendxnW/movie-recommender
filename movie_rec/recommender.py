from .nlp_utils import RecommendMovie


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

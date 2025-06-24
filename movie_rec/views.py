from django.shortcuts import render
from .chat_bot import ChatBot
from .nlp_utils import RecommendMovie

def movie_recommender_view(request):
    if request.method == "POST":
        user_input = request.POST.get("movie_prompt")
        recommender = RecommendMovie()
        genre = recommender.classify_genre(user_input)
        return render(request, "results.html", {"genre": genre})
    return render(request, "recommend.html")

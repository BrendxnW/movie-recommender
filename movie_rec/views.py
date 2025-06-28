from django.shortcuts import render
from .nlp_utils import RecommendMovie, GreetingPrompt


def greet_view(request):
    context = {
        "greeting": None,
        "feature": None,
        "movie_result": None,
    }

    if request.method == "POST":
        if "name" in request.POST:
            name = request.POST.get("name", "").capitalize()
            if name:
                greeter = GreetingPrompt(name)
                greeting = greeter.generate_prompt()
                request.session['name'] = name
                request.session['step'] = 'choose_feature'
                context['greeting'] = greeting

        elif "feature" in request.POST:
            feature = request.POST.get("feature")
            if feature == 'back':
                request.session.flush()
                context = {}
            elif feature == 'recommender':
                request.session['step'] = 'recommender'
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = 'recommender'
                context['show_recommender_prompt'] = True
            else:
                request.session['step'] = feature
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = feature

        elif "action" in request.POST:
            if request.POST.get("action") == "back":
                request.session['step'] = 'choose_feature'
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()

        elif "movie_prompt" in request.POST:
            user_input = request.POST.get("movie_prompt")
            recommender = RecommendMovie()
            genre = recommender.classify_genre(user_input)
            context['movie_result'] = f"Sounds like you're in the mood for a {genre} movie.\n Here is a list of movie I recommend!"
            context['feature'] = 'recommender'
            context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()

    else:
        request.session.flush()

    return render(request, "movie_rec/recommend.html", context)




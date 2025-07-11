from django.shortcuts import render
from .nlp_utils import RecommendMovie, GreetingPrompt
from .tmdb_API import get_movies_by_genre, InvalidGenreError


def greet_view(request):
    context = {
        "greeting": None,
        "feature": None,
        "movie_result": None,
    }

    step = request.session.get('step', 'greeting')

    if request.method == "POST":
        if request.POST.get("action") == "back":
            # Go back to the previous step
            if step == 'feature':
                # Go back to greeting (name input)
                request.session['step'] = 'greeting'
                context['greeting'] = None
                context['feature'] = None
                context['movie_result'] = None
            elif step == 'recommender':
                # Go back to feature selection
                request.session['step'] = 'feature'
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = None
                context['movie_result'] = None
            elif step == 'greeting':
                # Already at the first step, maybe flush session
                request.session.flush()
                context = {
                    "greeting": None,
                    "feature": None,
                    "movie_result": None,
                }

        elif "name" in request.POST:
            name = request.POST.get("name", "").capitalize()
            if name:
                greeter = GreetingPrompt(name)
                greeting = greeter.generate_prompt()
                request.session['name'] = name
                request.session['step'] = 'feature'
                context['greeting'] = greeting

        elif "feature" in request.POST:
            feature = request.POST.get("feature")
            if feature == 'recommender':
                request.session['step'] = 'recommender'
                context['greeting'] = None
                context['feature'] = 'recommender'
            else:
                request.session['step'] = feature
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = feature


        elif "movie_prompt" in request.POST:
            user_input = request.POST.get("movie_prompt")
            recommender = RecommendMovie()
            genre = recommender.classify_genre(user_input)

            try:
                movie_list = get_movies_by_genre(genre)
                if movie_list and isinstance(movie_list, list) and isinstance(movie_list[0], dict):
                    context['movie_options'] = movie_list
                    request.session['movie_options'] = movie_list
                else:
                    context['movie_result'] = f"Sorry, I couldn't find any good {genre} movies right now."
            except InvalidGenreError as e:
                context['movie_result'] = str(e)
            except Exception as e:
                context['movie_result'] = "Sorry, something went wrong while fetching recommendations."

            context['feature'] = 'recommender'
            context['greeting'] = None

        elif "selected_movie" in request.POST:
            selected_title = request.POST.get("selected_movie")
            movies = request.session.get("movie_options", [])
            selected = next((m for m in movies if m["title"] == selected_title), None)

            if selected:
                context['selected_title'] = selected["title"]
                context['selected_description'] = selected["description"]
                context['selected_trailer'] = selected.get("trailer_url")
                context['movie_options'] = movies

    else:
        request.session['step'] = 'greeting'
        context = {
            "greeting": None,
            "feature": None,
            "movie_result": None,
        }

    step = request.session.get('step', 'greeting')
    if step == 'greeting':
        context['greeting'] = None
        context['feature'] = None
    elif step == 'feature':
        context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
        context['feature'] = None
    elif step == 'recommender':
        context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
        context['feature'] = 'recommender'

    return render(request, "movie_rec/recommend.html", context)




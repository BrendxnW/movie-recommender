from django.shortcuts import render
from .nlp_utils import RecommendMovie, GreetingPrompt


def greet_view(request):
    # Default context
    context = {
        "greeting": None,
        "feature": None,
        "movie_result": None,
    }

    # Get current step from session, default to greeting
    step = request.session.get('step', 'greeting')

    if request.method == "POST":
        if request.POST.get("action") == "back":
            # Go back to the previous step
            if step == 'feature':
                # Go back to greeting (name input)
                request.session['step'] = 'greeting'
                context['greeting'] = None
                context['feature'] = None
            elif step == 'recommender':
                # Go back to feature selection
                request.session['step'] = 'feature'
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = None
            elif step == 'greeting':
                # Already at the first step, maybe flush session
                request.session.flush()
                context = {
                    "greeting": None,
                    "feature": None,
                    "movie_result": None,
                }
            # Add more elifs for other features if needed

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
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = 'recommender'
            else:
                request.session['step'] = feature
                context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()
                context['feature'] = feature

        elif "movie_prompt" in request.POST:
            user_input = request.POST.get("movie_prompt")
            recommender = RecommendMovie()
            genre = recommender.classify_genre(user_input)
            context['movie_result'] = f"Sounds like you're in the mood for a {genre} movie.\n Here is a list of movie I recommend!"
            context['feature'] = 'recommender'
            context['greeting'] = GreetingPrompt(request.session.get('name')).generate_prompt()

    else:
        # On GET, start at greeting
        request.session['step'] = 'greeting'
        context = {
            "greeting": None,
            "feature": None,
            "movie_result": None,
        }

    # Set context for template based on step
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




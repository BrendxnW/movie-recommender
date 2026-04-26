import os
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .nlp_utils import RecommendMovie, Remixer, ClassifyIntent, FindMovie
from .tmdb_API import get_movies_by_genre, InvalidGenreError, get_movie_plot
from .forms import CustomUserCreationForm


_movie_titles = None

def load_imdb_titles():
    global _movie_titles
    if _movie_titles is None:
        csv_path = os.getenv(
            "FILTERED_MOVIES_PATH",
            os.path.join("fine_tune", "data", "filtered_movies.csv")
        )

        try:
            df = pd.read_csv(csv_path)
            title_column = df.columns[0]
            _movie_titles = df[title_column].dropna().unique().tolist()
        except Exception as e:
            print(f"Error loading movie titles: {e}")
            _movie_titles = []
    return _movie_titles


def login(request):
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def home(request):
    return render(request,"home.html")

def recommender(request):
    context = {
        "feature": "recommender",
        "movie_result": None,
        "response": None,
        "selected_title": None,
    }

    chat_history = request.session.get("chat_history", [])

    if request.method == "POST":
        action = request.POST.get("action")


        if action == "submit_prompt":
            user_input = request.POST.get("movie_prompt")

            chat_history.append({
                "sender": "user",
                "message": user_input
            })

            intent_finder = ClassifyIntent()
            intent = intent_finder.classify_intent(user_input)
            print(f"Classified intent: {intent}")

            if intent == "genre":
                recommender = RecommendMovie()
                genres = recommender.classify_genre(user_input)

                if isinstance(genres, str):
                    genres = [genres]

                request.session['current_genres'] = genres
                request.session['current_genre'] = ", ".join(genres) if len(genres) > 1 else genres[0]

                genre_display = ", ".join(genres) if len(genres) > 1 else genres[0]

                try:
                    movie_list = get_movies_by_genre(genres)
                    if movie_list and isinstance(movie_list, list) and len(movie_list) > 0:
                        context['movie_result'] = (
                            f"Sounds like you're in the mood for a {genre_display} movie.\n"
                            f"Here are some movies I recommend:"
                        )

                        context['movie_options'] = movie_list
                        request.session['movie_options'] = movie_list
                    else:
                        context['movie_result'] = f"Sorry, I couldn't find any good {genre_display} movies right now."
                except InvalidGenreError as e:
                    context['movie_result'] = str(e)
                except Exception as e:
                    context['movie_result'] = "Sorry, something went wrong while fetching recommendations."

                context['feature'] = 'recommender'
                context['greeting'] = None


            elif intent == "description":
                recommender = FindMovie()
                movie_suggestions = recommender.suggest(user_input)
                if movie_suggestions:
                    request.session['reroll_movies'] = movie_suggestions[1:]  # save the rest for reroll
                    request.session.modified = True
                    # Prepare the list of 5 movies for display
                    context['movie_options'] = movie_suggestions[:5]
                    request.session['movie_options'] = movie_suggestions[:5]
                    # Build a string listing the 5 movies nicely
                    titles_list = "\n- ".join([movie['title'] for movie in movie_suggestions[:5]])
                    context['movie_result'] = f"I suggest these movies based on your description:\n- {titles_list}"
                else:
                    context['movie_result'] = "Sorry, couldn't find any matches."
            else:
                context['movie_result'] = "Sorry, I couldn't understand that."
            context['feature'] = 'recommender'
            context['greeting'] = None


        elif "selected_movie" in request.POST:
            selected_title = request.POST.get("selected_movie")
            movies = request.session.get("movie_options", [])
            selected = next((m for m in movies if m["title"] == selected_title), None)

            if selected:
                description = selected.get('overview') or get_movie_plot(selected_title)
                context['selected_title'] = selected["title"]
                context['selected_description'] = description
                context['selected_trailer'] = selected.get("trailer_url")
                context['movie_options'] = movies
                context['movie_result'] = request.session.get('movie_result')
                context['feature'] = 'recommender'
                context['greeting'] = None


            request.session["chat_history"] = chat_history
            request.session.modified = True


        elif request.POST.get("action") == "more_movies":
            current_genre = request.session.get('current_genre', [])
            if current_genre:
                try:
                    movie_list = get_movies_by_genre(current_genre)
                    if movie_list:
                        context['movie_result'] = f"Here are 5 more {current_genre} movies:"
                        context['movie_options'] = movie_list
                        request.session['movie_options'] = movie_list
                    else:
                        context['movie_result'] = f"Sorry, couldn't find any more {current_genre} movies right now."
                except Exception:
                    context['movie_result'] = "Sorry, something went wrong while fetching more recommendations."


        elif request.POST.get("action") == "reroll":
            reroll_list = request.session.get('reroll_movies', [])
            if reroll_list:
                next_movie = reroll_list.pop(0)
                request.session['reroll_movies'] = reroll_list
                request.session.modified = True
                context['movie_options'] = [next_movie]
                request.session['movie_options'] = [next_movie]
                context['movie_result'] = f"How about this one instead?\n- {next_movie['title']}"
            else:
                context['movie_result'] = "No more rerolls available!"

        
        chat_history.append({
            "sender": "bot",
            "message": context['movie_result']
        })

        request.session["chat_history"] = chat_history
        request.session.modified = True

        if action == "clear_chat":
            request.session["chat_history"] = []
            request.session.pop("movie_options", None)
            request.session.pop("reroll_movies", None)
            request.session.pop("current_genre", None)
            request.session.modified = True

    context["chat_history"] = chat_history
    return render(request, "recommender.html", context)



def remixer(request):
    context = {
    "feature": "remixer",
    "movie_result": None,
    "response": None,
    "imdb_movies": load_imdb_titles(),
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "submit_remix":
            movie1 = request.POST.get("movie1")
            movie2 = request.POST.get("movie2")
            context['imdb_movies'] = load_imdb_titles()

            if movie1 and movie2:
                try:
                    plot1 = get_movie_plot(movie1)
                    plot2 = get_movie_plot(movie2)
                    vibes = request.POST.getlist("vibe")

                    remixer = Remixer()
                    remixed_plot = remixer.plot_mixer(plot1, plot2, vibes=vibes)

                    context['response'] = remixed_plot
                    context['feature'] = 'remixer'
                    context['greeting'] = None
                    request.session['step'] = 'remixer'

                except Exception as e:
                    context['response'] = f"Sorry, something went wrong while remixing the plots: {str(e)}"
                    context['feature'] = 'remixer'
                    context['greeting'] = None

            else:
                context['response'] = "Please enter both movie titles."
                context['feature'] = 'remixer'
                context['greeting'] = None


    return render(request,"remixer.html", context)


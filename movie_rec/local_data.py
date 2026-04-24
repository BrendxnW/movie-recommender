import pandas as pd
import ast
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

keywords_path = os.getenv(
    "KEYWORDS_PATH",
    os.path.join(BASE_DIR, "fine_tune", "data", "keywords.csv")
)

movies_path = os.getenv(
    "MOVIES_PATH",
    os.path.join(BASE_DIR, "fine_tune", "data", "movies_metadata.csv")
)

keywords_df = pd.read_csv(keywords_path)
movies_df = pd.read_csv(movies_path, low_memory=False)

keywords_df['keywords'] = keywords_df['keywords'].apply(ast.literal_eval)

keyword_to_movies = {}
for _, row in keywords_df.iterrows():
    movie_id = int(row['id'])
    for kw in row['keywords']:
        keyword_name = kw['name'].lower()
        keyword_to_movies.setdefault(keyword_name, []).append(movie_id)

movie_id_to_info = {}
for _, row in movies_df.iterrows():
    try:
        movie_id = int(row['id'])
        movie_id_to_info[movie_id] = {
            "title": row['title'],
            "year": row.get('release_date', '')[:4] if pd.notnull(row.get('release_date')) else ''
        }
    except ValueError:
        continue

with open("description_data.py", "w", encoding="utf-8") as f:
    f.write("keyword_to_movies = " + repr(keyword_to_movies) + "\n\n")
    f.write("movie_id_to_info = " + repr(movie_id_to_info) + "\n")

print("Successful!")
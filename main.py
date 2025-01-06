import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# TMDb API setup
API_KEY = os.getenv('TMDB_API_KEY')  # Load API key from environment variable
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# Fetch top-rated movies
def get_top_rated_movies(top_n=12):
    try:
        url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return [
            {
                "original_title": movie["title"],
                "poster_path": IMAGE_URL + movie["poster_path"] if movie["poster_path"] else "",
                "rating": movie["vote_average"]
            }
            for movie in data["results"][:top_n]
        ]
    except Exception as e:
        print(f"Error fetching top-rated movies: {e}")
        return []

# Fetch genres
def get_genres():
    try:
        url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return {genre["name"]: genre["id"] for genre in data["genres"]}
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return {}

# Recommend movies with additional filters
def recommend_movies(preferred_genre_id, selected_movie_titles, rating, language, duration, popularity, release_year_range, actor=None, director=None, top_n=12):
    try:
        params = {
            "api_key": API_KEY,
            "with_genres": preferred_genre_id,
            "vote_average.gte": rating,
            "with_runtime.gte": duration[0],
            "with_runtime.lte": duration[1],
            "language": "en-US",
            "sort_by": popularity,  # "popularity.desc" for blockbusters, "popularity.asc" for hidden gems
            "with_original_language": language,
            "release_date.gte": release_year_range[0],
            "release_date.lte": release_year_range[1],
            "page": 1,
        }

        if actor:
            actor_response = requests.get(f"{BASE_URL}/search/person?api_key={API_KEY}&query={actor}")
            actor_response.raise_for_status()
            actors = actor_response.json()["results"]
            if actors:
                params["with_cast"] = actors[0]["id"]

        if director:
            director_response = requests.get(f"{BASE_URL}/search/person?api_key={API_KEY}&query={director}")
            director_response.raise_for_status()
            directors = director_response.json()["results"]
            if directors:
                params["with_crew"] = directors[0]["id"]

        url = f"{BASE_URL}/discover/movie"
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return [
            {
                "original_title": movie["title"],
                "poster_path": IMAGE_URL + movie["poster_path"] if movie["poster_path"] else "",
                "rating": movie["vote_average"],
                "overview": movie.get("overview", "No overview available.")
            }
            for movie in data["results"][:top_n]
        ]
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

@app.route('/')
def index():
    top_movies = get_top_rated_movies()
    genres = get_genres()
    return render_template('index.html', top_movies=top_movies, genres=genres.keys())

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie_titles = request.form.getlist('movies')
    preferred_genre = request.form['genre']
    genres = get_genres()
    genre_id = genres.get(preferred_genre, 28)

    rating = float(request.form.get("rating", 0))
    language = request.form.get("language", "en")
    duration = [int(request.form.get("min_duration", 0)), int(request.form.get("max_duration", 500))]
    popularity = request.form.get("popularity", "popularity.desc")
    release_year_range = [request.form.get("release_year_start", "1900"), request.form.get("release_year_end", "2024")]
    actor = request.form.get("actor")
    director = request.form.get("director")

    recommendations = recommend_movies(
        preferred_genre_id=genre_id,
        selected_movie_titles=selected_movie_titles,
        rating=rating,
        language=language,
        duration=duration,
        popularity=popularity,
        release_year_range=release_year_range,
        actor=actor,
        director=director
    )
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

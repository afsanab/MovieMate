from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# TMDb API setup
API_KEY = "API_KEY_GOES_HERE"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# Fetch top-rated movies using the API
def get_top_rated_movies(top_n=18):
    try:
        url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract movie details
        movies = [
            {
                "original_title": movie["title"],
                "poster_path": IMAGE_URL + movie["poster_path"] if movie["poster_path"] else "",
                "rating": movie["vote_average"]
            }
            for movie in data["results"][:top_n]
        ]
        return movies
    except Exception as e:
        print(f"Error fetching top-rated movies: {e}")
        return []

# Fetch genres from TMDb
def get_genres():
    try:
        url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract genre names and IDs
        genres = {genre["name"]: genre["id"] for genre in data["genres"]}
        return genres
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return {}

# Fetch movies by genre
def recommend_movies_by_genre(genre_id, top_n=10):
    try:
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract movie details
        movies = [
            {
                "original_title": movie["title"],
                "poster_path": IMAGE_URL + movie["poster_path"] if movie["poster_path"] else "",
                "rating": movie["vote_average"]
            }
            for movie in data["results"][:top_n]
        ]
        return movies
    except Exception as e:
        print(f"Error fetching movies by genre: {e}")
        return []

# Flask Routes
@app.route('/')
def index():
    top_movies = get_top_rated_movies()
    genres = get_genres()
    return render_template('index.html', top_movies=top_movies, genres=genres.keys())

@app.route('/recommend', methods=['POST'])
def recommend():
    preferred_genre = request.form['genre']
    genres = get_genres()
    genre_id = genres.get(preferred_genre, 28)  # Default to Action if genre not found
    recommendations = recommend_movies_by_genre(genre_id)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

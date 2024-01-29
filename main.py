from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

def get_top_rated_movies(file_path, top_n=20):
    # Load the dataset
    movies_df = pd.read_csv(file_path)

    # Convert 'popularity' to numeric, setting errors to NaN
    movies_df['popularity'] = pd.to_numeric(movies_df['popularity'], errors='coerce')

    # Optionally handle missing/NaN values
    # For example, you can drop rows with NaN in either 'vote_average' or 'popularity'
    movies_df.dropna(subset=['vote_average', 'popularity'], inplace=True)

    # Normalize 'vote_average' and 'popularity'
    movies_df['vote_average_norm'] = movies_df['vote_average'] / movies_df['vote_average'].max()
    movies_df['popularity_norm'] = movies_df['popularity'] / movies_df['popularity'].max()

    # Define weights
    weight_vote_average = 0.5
    weight_popularity = 0.5

    # Calculate combined score
    movies_df['score'] = (movies_df['vote_average_norm'] * weight_vote_average) + (movies_df['popularity_norm'] * weight_popularity)

    # Filter out movies with low vote counts to ensure the ratings are reliable
    movies_df = movies_df[movies_df['vote_count'] > 50]

    # Sort by 'score' and select the top_n movies
    top_movies_df = movies_df[['original_title', 'vote_average', 'popularity', 'score']].sort_values(by='score', ascending=False).head(top_n)

    # Convert to a list of dictionaries
    top_movies_list = top_movies_df.to_dict('records')

    return top_movies_list

def extract_genres(file_path):
    # Load the dataset
    movies_df = pd.read_csv(file_path)

    # Initialize an empty set to store unique genres
    genres = set()

    # Iterate over each row and extract genres
    for genre_list in movies_df['genres']:
        try:
            # Parse the genre string into a list
            genre_dicts = json.loads(genre_list.replace("'", '"'))

            # Add each genre to the set
            for genre in genre_dicts:
                genres.add(genre['name'])
        except json.JSONDecodeError:
            continue  # Skip rows where the genre data is not properly formatted

    return sorted(genres)  # Return a sorted list of unique genres


def recommend_movies_by_genre(genre, file_path, top_n=10):
    # Load the dataset
    movies_df = pd.read_csv(file_path)

    # Function to parse genres and check if the selected genre is in the movie's genres
    def is_genre_present(genres_str, selected_genre):
        try:
            genres = json.loads(genres_str.replace("'", '"'))
            for g in genres:
                if g['name'] == selected_genre:
                    return True
        except json.JSONDecodeError:
            return False
        return False

    # Filter movies by the selected genre
    movies_df['is_genre'] = movies_df['genres'].apply(lambda x: is_genre_present(x, genre))
    genre_movies_df = movies_df[movies_df['is_genre']]

    # Assuming you want to recommend the highest-rated movies in the selected genre
    top_movies = genre_movies_df[['original_title', 'vote_average']].sort_values(by='vote_average', ascending=False).head(top_n)

    return top_movies.to_dict('records')

@app.route('/')
def index():
    top_movies = get_top_rated_movies('data/movies_metadata.csv')
    genres = extract_genres('data/movies_metadata.csv')
    return render_template('index.html', top_movies=top_movies, genres=genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movies = request.form.getlist('movies')
    preferred_genre = request.form['genre']
    recommendations = recommend_movies_by_genre(preferred_genre, 'data/movies_metadata.csv')
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd

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

@app.route('/')
def index():
    top_movies = get_top_rated_movies('data/movies_metadata.csv')
    return render_template('index.html', top_movies=top_movies)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movies = request.form.getlist('movies')
    # Add your logic here to generate recommendations based on selected_movies
    #recommendations = your_recommendation_function(selected_movies)
    #return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

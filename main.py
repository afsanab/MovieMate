from flask import Flask, render_template, request
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Your movie recommendation function goes here
def recommend_movies(user_selected_movies, user_preference_genre):
    
    # Load the dataset
    movies_df = pd.read_csv('movies_metadata.csv')
    ratings_df = pd.read_csv('ratings.csv')

    # Convert fields to appropriate data types and handle missing values
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')
    movies_df = movies_df.dropna(subset=['release_date'])
    movies_df['year'] = movies_df['release_date'].dt.year

    # Preprocess Genres Data
    def parse_genres(genres_str):
        genres = json.loads(genres_str.replace('\'', '"'))
        return ' '.join(genre['name'] for genre in genres)

    movies_df['genres'] = movies_df['genres'].apply(parse_genres)

    # Select 20 most popular movies
    # Assuming popularity is based on the number of ratings
    popular_movies = ratings_df['movieId'].value_counts().head(20).index.tolist()
    popular_movies_df = movies_df[movies_df['id'].isin([str(id) for id in popular_movies])]

    # Display the 20 most popular movies
    print("20 Most Popular Movies:")
    print(popular_movies_df[['title', 'genres']])

    # User selects 5 movies (for demonstration, select first 5)
    user_selected_movies = popular_movies_df.head(5)

    # User chooses a genre
    user_preference_genre = request.form.get('genre')

    # Vectorize the genre data
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres'])

    # Transform user selected movies' genres into the vector space
    user_movies_genres = ' '.join(user_selected_movies['genres'])
    user_pref_vector = tfidf.transform([user_movies_genres + ' ' + user_preference_genre])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(user_pref_vector, tfidf_matrix)

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[0]))

    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the top 3 most similar movies
    top_3_movies = sim_scores[:3]

    # Get movie titles
    movie_indices = [i[0] for i in top_3_movies]
    recommended_movies = movies_df['title'].iloc[movie_indices]

    print("\nTop 3 Recommended Movies:")
    print(recommended_movies)
    
    return recommended_movies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movies = request.form.getlist('movies')
    preferred_genre = request.form['genre']
    recommendations = recommend_movies(selected_movies, preferred_genre)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def get_top_rated_movies(file_path, top_n=20):
    # Load the dataset
    movies_df = pd.read_csv(file_path)

    # Filter out movies with low vote counts to ensure the ratings are reliable
    movies_df = movies_df[movies_df['vote_count'] > 50]

    # Sort by vote_average and select the top_n movies
    top_movies_df = movies_df[['original_title', 'vote_average']].sort_values(by='vote_average', ascending=False).head(top_n)

    # Convert the DataFrame to a list of dictionaries
    top_movies_list = top_movies_df.to_dict('records')

    return top_movies_list

@app.route('/')
def index():
    top_movies = get_top_rated_movies('data/movies_metadata.csv')
    return render_template('index.html', top_movies=top_movies)

if __name__ == '__main__':
    app.run(debug=True)

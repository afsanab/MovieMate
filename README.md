# MovieMate

MovieMate is a dynamic web application that provides tailored movie recommendations based on user preferences. The app leverages the powerful [TMDb API](https://www.themoviedb.org/) to fetch data on movies, including top-rated films, genres, and detailed information for recommendations.

## Features
- **Top-Rated Movies:** View a list of top-rated movies with posters and ratings.
- **Personalized Recommendations:** Select favorite movies and set preferences such as genres, ratings, release years, and more to get customized movie recommendations.
- **Advanced Filters:** Narrow down recommendations by runtime, language, popularity, actor, and director.
- **Responsive Design:** Fully optimized for mobile and desktop viewing.

## Deployment
The app is live and accessible at: [MovieMate](https://moviemate-3r8ddb8p8-afsanabs-projects.vercel.app)

## API
This project utilizes the [TMDb API](https://www.themoviedb.org/) for movie data. **Note:** This product uses the TMDb API but is not endorsed or certified by TMDb.

### API Features Used
- **Top-Rated Movies:** Data fetched from `/movie/top_rated` endpoint.
- **Genres:** Data fetched from `/genre/movie/list` endpoint.
- **Discover Movies:** Customized movie searches using the `/discover/movie` endpoint with advanced filtering options.

## Technologies Used
- **Frontend:**
  - HTML5, CSS3 (Responsive styling with custom themes).
  - JavaScript for dynamic interaction.
- **Backend:**
  - Python with Flask framework for API integration and server-side logic.
  - `python-dotenv` for secure API key management.
- **Hosting:**
  - Deployed on [Vercel](https://vercel.com/) for fast and reliable hosting.

## Setup Instructions
To run this project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/afsanab/moviemate.git
   cd moviemate
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root.
   - Add the following line:
     ```env
     TMDB_API_KEY=your_api_key_here
     ```

5. **Run the app:**
   ```bash
   python main.py
   ```
   The app will run locally at `http://127.0.0.1:5000/`.

## Credits
This project is developed by [Afsana Bhuiyan](https://github.com/afsanab) and [Nadia Choudhury](https://github.com/nadiachoudhury) and leverages the [TMDb API](https://www.themoviedb.org/) for data.

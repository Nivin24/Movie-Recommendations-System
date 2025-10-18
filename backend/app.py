from flask import Flask, request, jsonify, render_template,send_from_directory
from flask_cors import CORS
import pickle
from dotenv import load_dotenv
import aiohttp, asyncio
import os


# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)  


# Load the model and data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Function to get recommendations
def recommend(movie):
    movie_lower = movie.lower()
    movie_titles_lower = movies['title'].str.lower()
    if movie_lower not in movie_titles_lower.values:
        return ["Movie not found in database."]
    
    index = movie_titles_lower[movie_titles_lower == movie_lower].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = [movies.iloc[i[0]].title for i in movie_list]

    return recommended_movies

# Serve JS file explicitly
@app.route('/script.js')
def serve_js():
    frontend_dir = os.path.join(os.path.dirname(__file__), '../frontend')
    return send_from_directory(frontend_dir, 'script.js')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    data = request.get_json()
    movie_name = data.get('movie', '').strip()
    print("Movie requested:", movie_name)

    if not movie_name:
        return jsonify({"error": "No movie name provided."}), 400

    recommendations = recommend(movie_name)
    return jsonify({"recommended_movies": recommendations})

import requests

@app.route('/poster/<movie_title>')
def get_poster(movie_title):
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')

    async def fetch_movie_details():
        async with aiohttp.ClientSession() as session:
            # Search for the movie
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
            async with session.get(search_url) as res:
                data = await res.json()
                if not data.get('results'):
                    return {
                        "poster_url": "https://via.placeholder.com/500x750?text=No+Poster",
                        "overview": "No description available."
                    }

                movie_data = data['results'][0]  # Take first result
                overview = movie_data.get('overview', "No description available.")
                poster_path = movie_data.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"

                return {
                    "poster_url": poster_url,
                    "overview": overview
                }

    details = asyncio.run(fetch_movie_details())
    return jsonify(details)
    
# Development

# if __name__ == '__main__':
#     app.run(debug=True)

# Deployment

if __name__ == '__main__':
    # For local testing
    from waitress import serve  # production-grade WSGI server
    port = int(os.environ.get('PORT', 5000))
    serve(app, host='0.0.0.0', port=port)
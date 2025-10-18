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
 

def download_file_from_google_drive(file_id, destination):
    if os.path.exists(destination):
        print(f"{destination} already exists, skipping download.")
        return

    URL = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(URL, stream=True)

    if response.status_code == 200:
        with open(destination, "wb") as f:
            for chunk in response.iter_content(32768):
                f.write(chunk)
        print(f"{destination} downloaded successfully.")
    else:
        raise Exception(f"Failed to download file: status code {response.status_code}")
    
MOVIES_FILE = 'movies.pkl'
SIMILARITY_FILE = 'similarity.pkl'

# Google Drive file IDs
MOVIES_FILE_ID = 'https://drive.google.com/file/d/1ZB2FRD8OfPTbyqIvtjjU4l0_hy8HGO5W/view?usp=sharing'
SIMILARITY_FILE_ID = 'https://drive.google.com/file/d/1DY28JITY5tpsqiWZrxqiWoHD5Dal6xYq/view?usp=sharing'

download_file_from_google_drive(MOVIES_FILE_ID, MOVIES_FILE)
download_file_from_google_drive(SIMILARITY_FILE_ID, SIMILARITY_FILE)

# Load the pickle files
with open(MOVIES_FILE, 'rb') as f:
    movies = pickle.load(f)

with open(SIMILARITY_FILE, 'rb') as f:
    similarity = pickle.load(f)
    
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
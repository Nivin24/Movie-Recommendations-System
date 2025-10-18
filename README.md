# Movie Recommendations System

A machine learning-based movie recommendation system that provides personalized movie suggestions using content-based filtering. The system features a Flask backend API and a modern web interface built with HTML/JavaScript.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Data Processing](#data-processing)
- [Training Workflow](#training-workflow)
- [API Endpoints](#api-endpoints)
- [Demo](#demo)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This Movie Recommendations System uses advanced machine learning techniques to analyze movie features and provide personalized recommendations. The system implements content-based filtering by analyzing movie attributes such as genres, keywords, cast, crew, and overview to find similar movies.

## ✨ Features

- **Content-Based Filtering**: Recommends movies based on similarity of features
- **RESTful API**: Flask-based backend API for serving recommendations
- **Modern Web Interface**: Clean and responsive frontend design
- **Real-time Recommendations**: Get instant movie suggestions
- **Comprehensive Movie Database**: Trained on extensive movie dataset
- **Scalable Architecture**: Backend and frontend separated for easy deployment

## 📁 Project Structure

```
Movie-Recommendations-System/
│
├── backend/                    # Flask backend application
│   ├── app.py                 # Main Flask application with API endpoints
│   ├── requirements.txt       # Python dependencies
│   ├── Procfile              # Deployment configuration
│   └── .DS_Store
│
├── frontend/                   # Web interface
│   ├── index.html            # Main HTML page
│   └── script.js             # Frontend JavaScript logic
│
├── notebooks/                  # Jupyter notebooks for training
│   └── movie_recommender_training.ipynb  # Model training notebook
│
├── .gitignore
└── .DS_Store
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework for API
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning library
- **Flask-Cors**: Cross-origin resource sharing
- **Waitress**: Production WSGI server
- **Requests**: HTTP library
- **Python-dotenv**: Environment variable management
- **aiohttp & asyncio**: Asynchronous HTTP operations
- **gdown**: Google Drive file downloader

### Frontend
- **HTML5**: Structure
- **JavaScript (ES6+)**: Frontend logic
- **CSS3**: Styling

### Machine Learning
- **TF-IDF Vectorization**: Text feature extraction
- **Cosine Similarity**: Similarity measurement
- **Content-Based Filtering**: Recommendation algorithm

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Nivin24/Movie-Recommendations-System.git
cd Movie-Recommendations-System
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up environment variables** (if needed)
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 How to Run

### Running the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Running the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `index.html` in your web browser, or serve it using a simple HTTP server:
```bash
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

## 📊 Data Processing

The system processes movie data through several stages:

### 1. **Data Loading**
   - Loads movie metadata and credits datasets
   - Merges datasets on movie ID

### 2. **Feature Engineering**
   - **Genres**: Extracts genre names from JSON format
   - **Keywords**: Processes movie keywords
   - **Cast**: Extracts top actors (limited to top 3)
   - **Crew**: Identifies director information
   - **Overview**: Uses movie plot descriptions

### 3. **Text Processing**
   - Removes spaces from multi-word names
   - Converts all text to lowercase
   - Combines all features into a single 'tags' column

### 4. **Vectorization**
   - Applies TF-IDF vectorization to convert text to numerical features
   - Limits to top 5000 features
   - Uses English stop words

### 5. **Similarity Computation**
   - Calculates cosine similarity between all movies
   - Creates a similarity matrix for fast lookups

## 🎓 Training Workflow

The training process is documented in the Jupyter notebook: `notebooks/movie_recommender_training.ipynb`

### Training Steps:

1. **Import Libraries**
   - NumPy, Pandas for data manipulation
   - Scikit-learn for ML operations

2. **Load Datasets**
   - `tmdb_5000_movies.csv`: Movie metadata
   - `tmdb_5000_credits.csv`: Cast and crew information

3. **Data Preprocessing**
   - Handle missing values
   - Parse JSON columns (genres, keywords, cast, crew)
   - Select relevant features

4. **Feature Extraction**
   - Create helper functions to extract names from JSON
   - Extract director from crew
   - Limit cast to top 3 actors
   - Combine overview and keywords

5. **Text Preprocessing**
   - Remove spaces ("Sam Worthington" → "SamWorthington")
   - Convert to lowercase
   - Create 'tags' by combining all features

6. **Vectorization and Similarity**
   - Apply CountVectorizer or TF-IDF
   - Set max_features=5000
   - Apply stop words
   - Compute cosine similarity matrix

7. **Model Export**
   - Save processed data using pickle
   - Export similarity matrix
   - Save movie titles and indices

### Key Functions:

```python
def recommend(movie):
    """Returns top 5 similar movies"""
    # Find movie index
    # Get similarity scores
    # Sort and return top matches
```

## 🔌 API Endpoints

### GET `/`
Returns API status and welcome message

**Response:**
```json
{
  "status": "success",
  "message": "Movie Recommendation API is running"
}
```

### POST `/recommend`
Get movie recommendations based on input

**Request Body:**
```json
{
  "movie": "Avatar"
}
```

**Response:**
```json
{
  "recommendations": [
    "Movie 1",
    "Movie 2",
    "Movie 3",
    "Movie 4",
    "Movie 5"
  ]
}
```

### GET `/movies`
Returns list of all available movies

**Response:**
```json
{
  "movies": ["Avatar", "Pirates of the Caribbean", ...]
}
```

## 🖼️ Demo

### Screenshots

#### Homepage
![Homepage](./screenshots/homepage.png)
*Main interface for searching and getting movie recommendations*

#### Recommendation Results
![Recommendations](./screenshots/recommendations.png)
*Example of personalized movie recommendations*

#### API Response
![API](./screenshots/api_response.png)
*Sample API response with movie suggestions*

> **Note**: Add screenshots to a `screenshots/` folder in the repository root to display demo images.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add comments for complex logic
- Test your changes before submitting
- Update documentation as needed

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Nivin24**
- GitHub: [@Nivin24](https://github.com/Nivin24)
- Repository: [Movie-Recommendations-System](https://github.com/Nivin24/Movie-Recommendations-System)

## 🙏 Acknowledgments

- Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
- Inspiration: Content-based filtering techniques
- Community: Open source contributors

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Content-Based Filtering](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

---

⭐ If you find this project helpful, please give it a star!

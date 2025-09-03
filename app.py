import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_analysis import MovieDataAnalyzer
from movie_recommender import MovieRecommender
import requests
import json
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="🎬 Chalchitra AI - Your Movie Magic Companion",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better alignment and centering
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        position: relative;
        overflow-x: hidden;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    .main::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Theme-aware overrides to ensure readability in both themes */
    :root[data-theme='light'] .main-title,
    :root[data-theme='light'] .main-subtitle,
    :root[data-theme='light'] .page-header,
    :root[data-theme='light'] .page-subtitle,
    :root[data-theme='light'] .center-text,
    :root[data-theme='light'] .left-text {
        color: #111111 !important;
    }

    :root[data-theme='dark'] .main-title,
    :root[data-theme='dark'] .main-subtitle,
    :root[data-theme='dark'] .page-header,
    :root[data-theme='dark'] .page-subtitle,
    :root[data-theme='dark'] .center-text,
    :root[data-theme='dark'] .left-text {
        color: #ffffff !important;
    }
    
    .movie-card {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        text-align: left;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
        color: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        margin: 5px 0;
        text-align: center;
        height: 38px;
        margin-top: 0;
    }
    
    .stTextInput > div > div > input {
        text-align: center;
        border-radius: 10px;
        height: 38px;
    }
    
    .search-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .search-input {
        flex: 1;
    }
    
    .search-button {
        flex-shrink: 0;
    }
    
    .stSelectbox > div > div > div {
        text-align: center;
    }
    
    .stSlider > div > div > div > div {
        text-align: center;
    }
    
    .stCheckbox > div > div {
        text-align: center;
    }
    
    .stSuccess, .stInfo, .stWarning, .stError {
        text-align: center;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .center-text {
        text-align: center !important;
    }
    
    .left-text {
        text-align: left !important;
    }
    
    .main-title {
        text-align: center !important;
        font-size: 3rem !important;
        margin-bottom: 1rem !important;
    }
    
    .main-subtitle {
        text-align: center !important;
        font-size: 1.2rem !important;
        margin-bottom: 2rem !important;
    }
    
    .page-header {
        text-align: center !important;
        margin-bottom: 2rem !important;
    }
    
    .page-subtitle {
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    
    .center-text {
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    
    .page-subtitle.center-text {
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    
    /* Floating particles effect */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .particle:nth-child(1) { left: 10%; animation-delay: 0s; }
    .particle:nth-child(2) { left: 20%; animation-delay: 1s; }
    .particle:nth-child(3) { left: 30%; animation-delay: 2s; }
    .particle:nth-child(4) { left: 40%; animation-delay: 3s; }
    .particle:nth-child(5) { left: 50%; animation-delay: 4s; }
    .particle:nth-child(6) { left: 60%; animation-delay: 5s; }
    .particle:nth-child(7) { left: 70%; animation-delay: 6s; }
    .particle:nth-child(8) { left: 80%; animation-delay: 7s; }
    .particle:nth-child(9) { left: 90%; animation-delay: 8s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(100vh) scale(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) scale(1); opacity: 0; }
    }
    
    /* Enhanced card effects */
    .movie-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        text-align: left;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
        color: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the movie data."""
    try:
        analyzer = MovieDataAnalyzer()
        movies_df, ratings_df, movies_with_ratings = analyzer.load_data()
        
        # Check if data was loaded successfully
        if movies_df is None or ratings_df is None or movies_with_ratings is None:
            st.error("❌ Failed to load dataset files. Please check the console for detailed error messages.")
            st.info("💡 Make sure the data files (movies.csv and ratings.csv) are in the correct location.")
            return None, None, None, None
            
        return movies_df, ratings_df, movies_with_ratings, analyzer
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None, None, None

@st.cache_resource
def create_recommender(movies_df, ratings_df):
    """Create and cache the movie recommender."""
    return MovieRecommender(movies_df, ratings_df)

def get_movie_poster(movie_title, api_key=None):
    """Get movie poster from TMDB API with better error handling."""
    if not api_key:
        return None
    
    try:
        # Clean movie title for better search
        clean_title = movie_title.split('(')[0].strip()
        
        # Search for the movie
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': api_key,
            'query': clean_title,
            'language': 'en-US',
            'page': 1,
            'include_adult': False
        }
        
        # Try to get poster with shorter timeout
        response = requests.get(search_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Get the first result with a poster
                for result in data['results']:
                    if result.get('poster_path'):
                        poster_url = f"https://image.tmdb.org/t/p/w500{result['poster_path']}"
                        return poster_url
        
        return None
    except requests.exceptions.Timeout:
        # Silently handle timeouts
        return None
    except requests.exceptions.ConnectionError:
        # Silently handle connection errors
        return None
    except Exception as e:
        # Log other errors but don't show to user
        print(f"Poster fetch error for {movie_title}: {str(e)}")
        return None

def display_movie_card(title, similarity_score, genres, avg_rating, rating_count, poster_url=None):
    """Display movie card with container usage."""
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if poster_url:
                try:
                    with st.container():
                        # Shorter timeout for poster download
                        response = requests.get(poster_url, timeout=15)
                        if response.status_code == 200:
                            image = Image.open(io.BytesIO(response.content))
                            image.thumbnail((150, 225), Image.Resampling.LANCZOS)
                            st.image(image, width=120, use_container_width=False)
                        else:
                            # Show placeholder if poster download fails
                            st.markdown("""
                            <div style="width: 120px; height: 180px; background: linear-gradient(45deg, #667eea, #764ba2); 
                                       display: flex; align-items: center; justify-content: center; border-radius: 10px; color: white; font-size: 2rem;">
                                🎬
                            </div>
                            """, unsafe_allow_html=True)
                except requests.exceptions.Timeout:
                    # Show placeholder for timeout
                    st.markdown("""
                    <div style="width: 120px; height: 180px; background: linear-gradient(45deg, #667eea, #764ba2); 
                               display: flex; align-items: center; justify-content: center; border-radius: 10px; color: white; font-size: 2rem;">
                        🎬
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    # Show placeholder for any other error
                    st.markdown("""
                    <div style="width: 120px; height: 180px; background: linear-gradient(45deg, #667eea, #764ba2); 
                               display: flex; align-items: center; justify-content: center; border-radius: 10px; color: white; font-size: 2rem;">
                        🎬
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Show placeholder when no poster URL
                st.markdown("""
                <div style="width: 120px; height: 180px; background: linear-gradient(45deg, #667eea, #764ba2); 
                           display: flex; align-items: center; justify-content: center; border-radius: 10px; color: white; font-size: 2rem;">
                    🎬
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**{title}**")
            st.markdown(f"Similarity: {similarity_score:.3f} | Rating: {avg_rating:.2f} | Votes: {rating_count:,}")
            st.markdown(f"Genres: {genres}")

def main():
    # Add floating particles background effect
    st.markdown("""
    <div class="particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main title with proper centering
    st.markdown('<h1 class="main-title">🎬 Chalchitra AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">🌟 Where AI Meets Cinema Magic - Discover Your Perfect Movie Match! 🎭</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle"><em>From Bollywood blockbusters to Hollywood classics, we\'ve got your next obsession covered!</em> ✨</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading movie data..."):
        movies_df, ratings_df, movies_with_ratings, analyzer = load_data()
    
    if movies_df is None or ratings_df is None:
        st.error("❌ Error: Could not load the dataset.")
        return
    
    # Create recommender
    recommender = create_recommender(movies_df, ratings_df)
    stats = recommender.get_dataset_stats()
    
    # Sidebar
    st.sidebar.markdown("## 🎯 Your Movie Journey")
    st.sidebar.markdown("*Navigate through the magic of cinema!* ✨")
    page = st.sidebar.selectbox(
        "Where would you like to go?",
        ["🏠 Home & Recommendations", "📊 Data Analysis", "🎭 Genre Explorer", "🔍 Search Movies", "⭐ Top Movies"]
    )
    
    # Get TMDB API Key from secrets (production) or fallback to demo key
    try:
        tmdb_api_key = st.secrets["tmdb"]["api_key"]
    except:
        # Fallback to demo key if secrets not available
        tmdb_api_key = "8c247ea0b4b56ed2ff7d41c9a833aa77"
    
    if page == "🏠 Home & Recommendations":
        st.markdown('<h2 class="page-header">🎬 Your Personal Movie Guru</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle"><strong>Lights, Camera, AI Action!</strong> 🎬✨</p>', unsafe_allow_html=True)
        
        # Dataset stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📽️ Total Movies</h3>
                <h2>{stats['total_movies']:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⭐ Total Ratings</h3>
                <h2>{stats['total_ratings']:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>👥 Unique Users</h3>
                <h2>{stats['unique_users']:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Avg Rating</h3>
                <h2>{stats['avg_rating']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendation section - better centered layout
        st.markdown('<h3 class="center-text">🎯 Tell Us What You Love, We\'ll Show You More!</h3>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle center-text"><em>Like a wise film critic who knows your taste better than you do!</em> 🧠✨</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the input section
        center_col1, center_col2, center_col3 = st.columns([1, 3, 1])
        
        with center_col2:
            if 'movie_input' in st.session_state:
                default_movie = st.session_state.movie_input
            else:
                default_movie = ""
            
            # Create a row for input and search button with better alignment
            input_col, button_col = st.columns([4, 1])
            
            with input_col:
                movie_input = st.text_input(
                    "🎬 Enter a movie title:",
                    value=default_movie,
                    placeholder="e.g., The Dark Knight, Inception, Pulp Fiction...",
                    key="movie_input_field"
                )
            
            with button_col:
                st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
                if st.button("🔍", help="Search for recommendations", key="search_button"):
                    if movie_input.strip():
                        st.session_state.movie_input = movie_input.strip()
                        st.rerun()
                    else:
                        st.warning("Please enter a movie title first!")
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Settings section - centered
        st.markdown('<h3 class="center-text">⚙️ Fine-Tune Your Movie Experience</h3>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle center-text"><em>Make it perfect, just like your favorite director!</em> 🎬🎯</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the settings
        settings_col1, settings_col2, settings_col3 = st.columns([1, 3, 1])
        
        with settings_col2:
            col1, col2, col3 = st.columns(3)
            with col1:
                n_recommendations = st.slider("Number of recommendations:", 5, 15, 10)
            with col2:
                min_rating_count = st.slider("Minimum ratings:", 1, 100, 10)
            with col3:
                min_avg_rating = st.slider("Minimum average rating:", 0.0, 5.0, 3.0, 0.1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            show_posters = st.checkbox("Show movie posters", value=True)
        
        # Get recommendations
        if movie_input:
            with st.spinner("🔍 Finding similar movies..."):
                recommendations = recommender.get_recommendations(
                    movie_input, 
                    n_recommendations=n_recommendations,
                    min_rating_count=min_rating_count,
                    min_avg_rating=min_avg_rating
                )
            
            if recommendations:
                st.success(f"🎯 You Selected: '{movie_input}'")
                st.info(f"🎬 **{len(recommendations)} cinematic treasures** that match your taste perfectly!")
                st.markdown('<p class="page-subtitle"><em>Our AI has handpicked these gems just for you!</em> ✨</p>', unsafe_allow_html=True)
                
                for i, (title, similarity_score, genres, avg_rating, rating_count) in enumerate(recommendations, 1):
                    poster_url = None
                    if show_posters and tmdb_api_key:
                        poster_url = get_movie_poster(title, tmdb_api_key)
                    
                    with st.container():
                        display_movie_card(title, similarity_score, genres, avg_rating, rating_count, poster_url)
            else:
                st.error(f"No movies found matching '{movie_input}'")
        
        # Popular movies suggestions
        st.markdown('<h3 class="center-text">💡 Can\'t Decide? Start With These Blockbusters!</h3>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle center-text"><em>Handpicked by our AI for guaranteed entertainment!</em> 🎭🔥</p>', unsafe_allow_html=True)
        popular_movies = [
            ("The Dark Knight", "Action|Crime|Drama"),
            ("Inception", "Action|Adventure|Sci-Fi"),
            ("Pulp Fiction", "Crime|Drama"),
            ("The Shawshank Redemption", "Drama"),
            ("Fight Club", "Drama")
        ]
        
        cols = st.columns(5)
        for i, (movie, genres) in enumerate(popular_movies):
            with cols[i]:
                button_text = movie.replace("The Shawshank Redemption", "Shawshank")
                if st.button(f"🎬 {button_text}", key=f"popular_{i}"):
                    st.session_state.movie_input = movie
                    st.rerun()
    
    elif page == "📊 Data Analysis":
        st.markdown('<h2 class="page-header">📊 Behind the Scenes - Movie Data Magic</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle"><strong>Numbers tell stories too!</strong> 📈✨</p>', unsafe_allow_html=True)
        
        insights = analyzer.get_basic_insights()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 **The Crowd Favorites**")
            st.markdown('<p class="page-subtitle"><em>Movies that stole everyone\'s hearts!</em> 💖</p>', unsafe_allow_html=True)
            for i, (_, row) in enumerate(insights['top_5_popular'].iterrows(), 1):
                st.markdown(f"""
                <div class="movie-card">
                    <strong>{i}. {row['title']}</strong><br>
                    Rating: {row['avg_rating']:.2f} | Votes: {row['rating_count']}<br>
                    <small>{row['genres']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⭐ **The Critics' Choice**")
            st.markdown('<p class="page-subtitle"><em>Perfection in every frame!</em> 🌟</p>', unsafe_allow_html=True)
            for i, (_, row) in enumerate(insights['top_5_rated'].iterrows(), 1):
                st.markdown(f"""
                <div class="movie-card">
                    <strong>{i}. {row['title']}</strong><br>
                    Rating: {row['avg_rating']:.2f} | Votes: {row['rating_count']}<br>
                    <small>{row['genres']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("### 📈 **The Numbers Tell a Story**")
        st.markdown('<p class="page-subtitle"><em>Charts that speak louder than words!</em> 📊✨</p>', unsafe_allow_html=True)
        figures = analyzer.create_visualizations()
        
        if figures:
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(figures['rating_distribution'])
            with col2:
                st.pyplot(figures['genre_distribution'])
            st.pyplot(figures['rating_vs_popularity'])
    
    elif page == "🎭 Genre Explorer":
        st.markdown('<h2 class="page-header">🎭 Genre Safari - Discover New Worlds!</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle"><strong>Every genre is a new adventure waiting to happen!</strong> 🌍🎬</p>', unsafe_allow_html=True)
        
        top_genres = [genre for genre, _ in stats['top_genres']]
        selected_genre = st.selectbox("Choose a genre to explore:", options=top_genres)
        
        if selected_genre:
            st.markdown(f'<h3 class="center-text">🎬 **{selected_genre} Universe Awaits!**</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="page-subtitle center-text"><em>Dive into the world of {selected_genre} magic!</em> 🌟</p>', unsafe_allow_html=True)
            genre_movies = recommender.get_movies_by_genre(selected_genre, n_movies=20)
            
            if genre_movies:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Movies in Genre", len(genre_movies))
                with col2:
                    avg_rating = sum(movie[2] for movie in genre_movies) / len(genre_movies)
                    st.metric("Average Rating", f"{avg_rating:.2f}")
                with col3:
                    total_votes = sum(movie[3] for movie in genre_movies)
                    st.metric("Total Votes", f"{total_votes:,}")
                
                st.markdown("---")
                
                for i, (title, genres, avg_rating, rating_count) in enumerate(genre_movies, 1):
                    poster_url = None
                    if tmdb_api_key:
                        poster_url = get_movie_poster(title, tmdb_api_key)
                    
                    with st.container():
                        display_movie_card(title, 0.0, genres, avg_rating, rating_count, poster_url)
            else:
                st.warning(f"No movies found in the {selected_genre} genre.")
    
    elif page == "🔍 Search Movies":
        st.markdown('<h2 class="page-header">🔍 Movie Detective - Find Hidden Gems!</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle"><strong>Your personal movie search engine!</strong> 🔍💎</p>', unsafe_allow_html=True)
        
        search_query = st.text_input("Search for movies by title or genre:", 
                                   placeholder="e.g., action, comedy, batman, sci-fi...")
        
        if search_query:
            with st.spinner("Searching..."):
                results = recommender.search_movies(search_query, n_results=20)
            
            if results:
                st.markdown(f'<h3 class="center-text">📋 **Search Results for \'{search_query}\'**</h3>', unsafe_allow_html=True)
                st.markdown(f'<p class="page-subtitle center-text"><em>Found {len(results)} movies that match your curiosity!</em> 🔍✨</p>', unsafe_allow_html=True)
                for title, genres, avg_rating, rating_count in results:
                    with st.container():
                        st.markdown(f"""
                        <div class="movie-card">
                            <strong>{title}</strong><br>
                            Rating: {avg_rating:.2f} | Votes: {rating_count}<br>
                            <small>{genres}</small>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning(f"No movies found matching '{search_query}'")
    
    elif page == "⭐ Top Movies":
        st.markdown('<h2 class="page-header">⭐ Hall of Fame - The Crème de la Crème!</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle"><strong>Only the best of the best make it here!</strong> 🏆✨</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            min_ratings = st.slider("Minimum number of ratings:", 10, 1000, 100)
        with col2:
            n_movies = st.slider("Number of movies to show:", 5, 50, 20)
        
        top_movies = recommender.get_movies_by_rating_range(
            min_rating=0.0, max_rating=5.0, min_ratings=min_ratings, n_movies=n_movies
        )
        
        if top_movies:
            st.markdown(f'<h3 class="center-text">🏆 **{len(top_movies)} Masterpieces That Define Cinema**</h3>', unsafe_allow_html=True)
            st.markdown('<p class="page-subtitle center-text"><em>These aren\'t just movies, they\'re experiences!</em> 🎭✨</p>', unsafe_allow_html=True)
            for i, (title, genres, avg_rating, rating_count) in enumerate(top_movies, 1):
                with st.container():
                    st.markdown(f"""
                    <div class="movie-card">
                        <strong>{i}. {title}</strong><br>
                        Rating: {avg_rating:.2f} | Votes: {rating_count}<br>
                        <small>{genres}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: inherit;">
        <h3>🎬 Chalchitra AI - Your Cinema Soulmate</h3>
        <p>✨ Where every recommendation is a love letter to cinema ✨</p>
        <p>🚀 From silent classics to modern masterpieces - your perfect match awaits!</p>
        <p>🎭 Because life is too short for bad movies!</p>
        <p style="font-size: 0.9rem; opacity: 0.7;">
            Made by ❤️ Aaryan Kumar | Movie Enthusiast & AI Explorer 🎭
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

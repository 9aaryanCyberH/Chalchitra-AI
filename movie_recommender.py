import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import re
from typing import List, Tuple, Optional

class MovieRecommender:
    def __init__(self, movies_df: pd.DataFrame, ratings_df: pd.DataFrame):
        """
        Initialize the MovieRecommender with movie and rating data.
        
        Args:
            movies_df (pd.DataFrame): DataFrame containing movie information
            ratings_df (pd.DataFrame): DataFrame containing rating information
        """
        self.movies_df = movies_df.copy()
        self.ratings_df = ratings_df.copy()
        self.movies_with_ratings = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.tfidf_vectorizer = None
        
        # Prepare the data
        self._prepare_data()
        self._build_similarity_matrix()
    
    def _prepare_data(self):
        """
        Prepare and merge movie and rating data.
        """
        # Calculate average ratings and rating counts
        rating_stats = self.ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        # Flatten column names
        rating_stats.columns = ['movieId', 'avg_rating', 'rating_count']
        
        # Merge with movies dataframe
        self.movies_with_ratings = self.movies_df.merge(
            rating_stats, on='movieId', how='left'
        )
        
        # Fill NaN values
        self.movies_with_ratings['avg_rating'] = self.movies_with_ratings['avg_rating'].fillna(0)
        self.movies_with_ratings['rating_count'] = self.movies_with_ratings['rating_count'].fillna(0)
        
        # Clean movie titles (remove year)
        self.movies_with_ratings['title_clean'] = self.movies_with_ratings['title'].apply(
            lambda x: re.sub(r'\(\d{4}\)', '', x).strip()
        )
        
        # Create a combined feature for TF-IDF (title + genres)
        self.movies_with_ratings['combined_features'] = (
            self.movies_with_ratings['title_clean'] + ' ' + 
            self.movies_with_ratings['genres'].str.replace('|', ' ')
        )
    
    def _build_similarity_matrix(self):
        """
        Build TF-IDF matrix and cosine similarity matrix.
        """
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        
        # Create TF-IDF matrix
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.movies_with_ratings['combined_features']
        )
        
        # Calculate cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
    
    def find_movie_by_title(self, movie_title: str, exact_match: bool = False) -> Optional[pd.Series]:
        """
        Find a movie by title (exact or partial match).
        
        Args:
            movie_title (str): Title of the movie to find
            exact_match (bool): Whether to require exact match
            
        Returns:
            pd.Series: Movie information if found, None otherwise
        """
        movie_title = movie_title.strip().lower()
        
        if exact_match:
            # Exact match
            mask = self.movies_with_ratings['title_clean'].str.lower() == movie_title
        else:
            # Partial match
            mask = self.movies_with_ratings['title_clean'].str.lower().str.contains(
                movie_title, na=False
            )
        
        matches = self.movies_with_ratings[mask]
        
        if len(matches) == 0:
            return None
        
        # If multiple matches, return the most popular one
        if len(matches) > 1:
            return matches.loc[matches['rating_count'].idxmax()]
        
        return matches.iloc[0]
    
    def get_recommendations(
        self, 
        movie_title: str, 
        n_recommendations: int = 5,
        min_rating_count: int = 5,
        min_avg_rating: float = 0.0
    ) -> List[Tuple[str, float, str, float, int]]:
        """
        Get movie recommendations based on a given movie title.
        
        Args:
            movie_title (str): Title of the movie to base recommendations on
            n_recommendations (int): Number of recommendations to return
            min_rating_count (int): Minimum number of ratings required
            min_avg_rating (float): Minimum average rating required
            
        Returns:
            List[Tuple]: List of (title, similarity_score, genres, avg_rating, rating_count)
        """
        # Find the movie
        movie = self.find_movie_by_title(movie_title)
        
        if movie is None:
            return []
        
        # Get the index of the movie
        movie_idx = movie.name
        
        # Get similarity scores for this movie
        sim_scores = list(enumerate(self.cosine_sim[movie_idx]))
        
        # Sort movies based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top similar movies (excluding the movie itself)
        sim_scores = sim_scores[1:n_recommendations*2]  # Get more to filter
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Get recommended movies
        recommended_movies = self.movies_with_ratings.iloc[movie_indices].copy()
        
        # Apply filters
        recommended_movies = recommended_movies[
            (recommended_movies['rating_count'] >= min_rating_count) &
            (recommended_movies['avg_rating'] >= min_avg_rating)
        ]
        
        # Take top N recommendations
        recommended_movies = recommended_movies.head(n_recommendations)
        
        # Create result list
        recommendations = []
        for idx, (_, movie) in enumerate(recommended_movies.iterrows()):
            # Find the similarity score for this movie
            sim_score = next(score for i, score in sim_scores if i == movie.name)
            
            recommendations.append((
                movie['title'],
                sim_score,
                movie['genres'],
                movie['avg_rating'],
                int(movie['rating_count'])
            ))
        
        return recommendations
    
    def get_popular_movies_by_genre(self, genre: str, n_movies: int = 5) -> List[Tuple[str, str, float, int]]:
        """
        Get popular movies of a specific genre.
        
        Args:
            genre (str): Genre to filter by
            n_movies (int): Number of movies to return
            
        Returns:
            List[Tuple]: List of (title, genres, avg_rating, rating_count)
        """
        # Filter movies by genre
        genre_movies = self.movies_with_ratings[
            self.movies_with_ratings['genres'].str.contains(genre, na=False)
        ]
        
        # Sort by popularity (rating count) and then by average rating
        popular_movies = genre_movies.sort_values(
            ['rating_count', 'avg_rating'], 
            ascending=[False, False]
        ).head(n_movies)
        
        return [
            (row['title'], row['genres'], row['avg_rating'], int(row['rating_count']))
            for _, row in popular_movies.iterrows()
        ]
    
    def get_movies_by_rating_range(
        self, 
        min_rating: float, 
        max_rating: float, 
        min_ratings: int = 10,
        n_movies: int = 10
    ) -> List[Tuple[str, str, float, int]]:
        """
        Get movies within a specific rating range.
        
        Args:
            min_rating (float): Minimum average rating
            max_rating (float): Maximum average rating
            min_ratings (int): Minimum number of ratings required
            n_movies (int): Number of movies to return
            
        Returns:
            List[Tuple]: List of (title, genres, avg_rating, rating_count)
        """
        filtered_movies = self.movies_with_ratings[
            (self.movies_with_ratings['avg_rating'] >= min_rating) &
            (self.movies_with_ratings['avg_rating'] <= max_rating) &
            (self.movies_with_ratings['rating_count'] >= min_ratings)
        ]
        
        # Sort by average rating
        top_movies = filtered_movies.sort_values('avg_rating', ascending=False).head(n_movies)
        
        return [
            (row['title'], row['genres'], row['avg_rating'], int(row['rating_count']))
            for _, row in top_movies.iterrows()
        ]
    
    def search_movies(self, query: str, n_results: int = 10) -> List[Tuple[str, str, float, int]]:
        """
        Search for movies by title or genre.
        
        Args:
            query (str): Search query
            n_results (int): Number of results to return
            
        Returns:
            List[Tuple]: List of (title, genres, avg_rating, rating_count)
        """
        query = query.lower()
        
        # Search in titles and genres
        mask = (
            self.movies_with_ratings['title_clean'].str.lower().str.contains(query, na=False) |
            self.movies_with_ratings['genres'].str.lower().str.contains(query, na=False)
        )
        
        results = self.movies_with_ratings[mask].sort_values(
            ['rating_count', 'avg_rating'], 
            ascending=[False, False]
        ).head(n_results)
        
        return [
            (row['title'], row['genres'], row['avg_rating'], int(row['rating_count']))
            for _, row in results.iterrows()
        ]
    
    def get_movies_by_genre(self, genre: str, n_movies: int = 20) -> List[Tuple[str, str, float, int]]:
        """
        Get movies by specific genre.
        
        Args:
            genre (str): Genre to filter by
            n_movies (int): Number of movies to return
            
        Returns:
            List[Tuple]: List of (title, genres, avg_rating, rating_count)
        """
        # Filter movies by genre
        mask = self.movies_with_ratings['genres'].str.contains(genre, na=False, case=False)
        genre_movies = self.movies_with_ratings[mask]
        
        # Sort by rating count (popularity) and then by average rating
        top_movies = genre_movies.sort_values(
            ['rating_count', 'avg_rating'], 
            ascending=[False, False]
        ).head(n_movies)
        
        return [
            (row['title'], row['genres'], row['avg_rating'], int(row['rating_count']))
            for _, row in top_movies.iterrows()
        ]
    
    def get_dataset_stats(self) -> dict:
        """
        Get basic statistics about the dataset.
        
        Returns:
            dict: Dictionary containing dataset statistics
        """
        return {
            'total_movies': len(self.movies_with_ratings),
            'total_ratings': len(self.ratings_df),
            'unique_users': self.ratings_df['userId'].nunique(),
            'avg_rating': self.ratings_df['rating'].mean(),
            'top_genres': self._get_top_genres(5)
        }
    
    def _get_top_genres(self, n: int = 5) -> List[Tuple[str, int]]:
        """
        Get top N genres by movie count.
        
        Args:
            n (int): Number of genres to return
            
        Returns:
            List[Tuple]: List of (genre, count)
        """
        all_genres = []
        for genres in self.movies_with_ratings['genres']:
            if pd.notna(genres):
                all_genres.extend(genres.split('|'))
        
        from collections import Counter
        genre_counts = Counter(all_genres)
        return genre_counts.most_common(n)

# Example usage
if __name__ == "__main__":
    # This would be used after loading the data
    from data_analysis import MovieDataAnalyzer
    
    analyzer = MovieDataAnalyzer()
    movies_df, ratings_df, _ = analyzer.load_data()
    
    if movies_df is not None and ratings_df is not None:
        recommender = MovieRecommender(movies_df, ratings_df)
        
        # Test recommendations
        recommendations = recommender.get_recommendations("The Dark Knight", n_recommendations=5)
        
        print("🎬 Recommendations for 'The Dark Knight':")
        for i, (title, sim_score, genres, avg_rating, rating_count) in enumerate(recommendations, 1):
            print(f"{i}. {title} (Similarity: {sim_score:.3f}, Rating: {avg_rating:.2f}, Votes: {rating_count})")
            print(f"   Genres: {genres}")
            print()

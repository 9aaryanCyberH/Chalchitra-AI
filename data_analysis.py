import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
import os
warnings.filterwarnings('ignore')

def get_data_file_path(filename):
    """
    Get the absolute path to a data file, trying multiple possible locations.
    
    Args:
        filename (str): Name of the data file (e.g., 'movies.csv')
        
    Returns:
        str: Absolute path to the file, or None if not found
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try multiple possible paths
    possible_paths = [
        os.path.join(script_dir, 'data', filename),
        os.path.join(script_dir, '..', 'data', filename),
        os.path.join(script_dir, '..', '..', 'data', filename),
        os.path.join(os.getcwd(), 'data', filename),
        os.path.join(os.getcwd(), filename),
        filename
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None

class MovieDataAnalyzer:
    def __init__(self, movies_path=None, ratings_path=None):
        """
        Initialize the MovieDataAnalyzer with dataset paths.
        
        Args:
            movies_path (str): Path to movies.csv file
            ratings_path (str): Path to ratings.csv file
        """
        # Try multiple possible paths for the data files
        if movies_path is None:
            movies_path = get_data_file_path('movies.csv')
            if movies_path is None:
                # Fallback to relative paths
                possible_movies_paths = [
                    'data/movies.csv',
                    './data/movies.csv',
                    '../data/movies.csv',
                    'movies.csv'
                ]
                for path in possible_movies_paths:
                    if os.path.exists(path):
                        movies_path = path
                        break
        
        if ratings_path is None:
            ratings_path = get_data_file_path('ratings.csv')
            if ratings_path is None:
                # Fallback to relative paths
                possible_ratings_paths = [
                    'data/ratings.csv',
                    './data/ratings.csv',
                    '../data/ratings.csv',
                    'ratings.csv'
                ]
                for path in possible_ratings_paths:
                    if os.path.exists(path):
                        ratings_path = path
                        break
        
        # If still no paths found, use defaults
        if movies_path is None:
            movies_path = 'data/movies.csv'
        if ratings_path is None:
            ratings_path = 'data/ratings.csv'
            
        self.movies_path = movies_path
        self.ratings_path = ratings_path
        self.movies_df = None
        self.ratings_df = None
        self.movies_with_ratings = None
        
        print(f"🔍 Data paths initialized:")
        print(f"   🎬 Movies: {self.movies_path}")
        print(f"   ⭐ Ratings: {self.ratings_path}")
        
    def load_data(self):
        """
        Load and prepare the MovieLens dataset.
        
        Returns:
            tuple: (movies_df, ratings_df, movies_with_ratings)
        """
        try:
            # Check if files exist
            if not os.path.exists(self.movies_path):
                print(f"❌ Movies file not found at: {self.movies_path}")
                print(f"Current working directory: {os.getcwd()}")
                print(f"Available files in current directory: {os.listdir('.')}")
                if os.path.exists('data'):
                    print(f"Files in data directory: {os.listdir('data')}")
                return None, None, None
                
            if not os.path.exists(self.ratings_path):
                print(f"❌ Ratings file not found at: {self.ratings_path}")
                print(f"Current working directory: {os.getcwd()}")
                return None, None, None
            
            # Load datasets
            self.movies_df = pd.read_csv(self.movies_path)
            self.ratings_df = pd.read_csv(self.ratings_path)
            
            print(f"✅ Data loaded successfully!")
            print(f"   Movies: {len(self.movies_df)} records from {self.movies_path}")
            print(f"   Ratings: {len(self.ratings_df)} records from {self.ratings_path}")
            
            # Calculate average ratings and rating counts
            rating_stats = self.ratings_df.groupby('movieId').agg({
                'rating': ['mean', 'count']
            }).reset_index()
            
            # Flatten column names
            rating_stats.columns = ['movieId', 'avg_rating', 'rating_count']
            
            # Merge movies with ratings to get average ratings
            self.movies_with_ratings = self.movies_df.merge(
                rating_stats,
                on='movieId',
                how='left'
            )
            
            # Fill NaN values
            self.movies_with_ratings['avg_rating'] = self.movies_with_ratings['avg_rating'].fillna(0)
            self.movies_with_ratings['rating_count'] = self.movies_with_ratings['rating_count'].fillna(0)
            
            return self.movies_df, self.ratings_df, self.movies_with_ratings
            
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            print(f"Current working directory: {os.getcwd()}")
            print("Please make sure the dataset files are accessible.")
            return None, None, None
        except Exception as e:
            print(f"❌ Unexpected error loading data: {e}")
            return None, None, None
    
    def get_basic_insights(self):
        """
        Extract basic insights from the dataset.
        
        Returns:
            dict: Dictionary containing basic insights
        """
        if self.movies_df is None or self.ratings_df is None:
            return None
            
        insights = {
            'total_movies': len(self.movies_df),
            'total_ratings': len(self.ratings_df),
            'unique_users': self.ratings_df['userId'].nunique(),
            'avg_rating': self.ratings_df['rating'].mean(),
            'rating_std': self.ratings_df['rating'].std(),
            'top_5_popular': self.get_top_popular_movies(5),
            'top_5_rated': self.get_top_rated_movies(5),
            'genre_distribution': self.get_genre_distribution(),
            'rating_distribution': self.get_rating_distribution()
        }
        
        return insights
    
    def get_top_popular_movies(self, n=5):
        """
        Get the top N most popular movies based on number of ratings.
        
        Args:
            n (int): Number of movies to return
            
        Returns:
            DataFrame: Top N popular movies
        """
        if self.movies_with_ratings is None:
            return None
            
        return self.movies_with_ratings.nlargest(n, 'rating_count')[
            ['title', 'genres', 'avg_rating', 'rating_count']
        ]
    
    def get_top_rated_movies(self, n=5, min_ratings=10):
        """
        Get the top N highest rated movies with minimum rating count.
        
        Args:
            n (int): Number of movies to return
            min_ratings (int): Minimum number of ratings required
            
        Returns:
            DataFrame: Top N rated movies
        """
        if self.movies_with_ratings is None:
            return None
            
        filtered_movies = self.movies_with_ratings[
            self.movies_with_ratings['rating_count'] >= min_ratings
        ]
        
        return filtered_movies.nlargest(n, 'avg_rating')[
            ['title', 'genres', 'avg_rating', 'rating_count']
        ]
    
    def get_genre_distribution(self):
        """
        Get the distribution of movie genres.
        
        Returns:
            dict: Genre distribution
        """
        if self.movies_df is None:
            return None
            
        # Split genres and count
        all_genres = []
        for genres in self.movies_df['genres']:
            if pd.notna(genres):
                all_genres.extend(genres.split('|'))
        
        genre_counts = Counter(all_genres)
        return dict(genre_counts.most_common())
    
    def get_rating_distribution(self):
        """
        Get the distribution of ratings.
        
        Returns:
            dict: Rating distribution
        """
        if self.ratings_df is None:
            return None
            
        rating_counts = self.ratings_df['rating'].value_counts().sort_index()
        return dict(rating_counts)
    
    def create_visualizations(self):
        """
        Create various visualizations for the dataset.
        
        Returns:
            dict: Dictionary containing matplotlib figures
        """
        if self.movies_df is None or self.ratings_df is None:
            return None
            
        figures = {}
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Rating Distribution
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        rating_counts = self.ratings_df['rating'].value_counts().sort_index()
        ax1.bar(rating_counts.index, rating_counts.values, color='skyblue', alpha=0.7)
        ax1.set_title('Distribution of Movie Ratings', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Rating', fontsize=12)
        ax1.set_ylabel('Number of Ratings', fontsize=12)
        ax1.grid(True, alpha=0.3)
        figures['rating_distribution'] = fig1
        
        # 2. Genre Distribution (Top 10)
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        genre_dist = self.get_genre_distribution()
        top_genres = dict(list(genre_dist.items())[:10])
        
        genres = list(top_genres.keys())
        counts = list(top_genres.values())
        
        bars = ax2.barh(genres, counts, color='lightcoral', alpha=0.7)
        ax2.set_title('Top 10 Movie Genres', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Number of Movies', fontsize=12)
        ax2.set_ylabel('Genre', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width + 10, bar.get_y() + bar.get_height()/2, 
                    str(counts[i]), ha='left', va='center', fontweight='bold')
        
        figures['genre_distribution'] = fig2
        
        # 3. Average Rating vs Number of Ratings
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        popular_movies = self.movies_with_ratings[
            self.movies_with_ratings['rating_count'] >= 10
        ]
        
        ax3.scatter(popular_movies['rating_count'], popular_movies['avg_rating'], 
                   alpha=0.6, color='mediumseagreen', s=30)
        ax3.set_title('Average Rating vs Number of Ratings', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Number of Ratings', fontsize=12)
        ax3.set_ylabel('Average Rating', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(popular_movies['rating_count'], popular_movies['avg_rating'], 1)
        p = np.poly1d(z)
        ax3.plot(popular_movies['rating_count'], p(popular_movies['rating_count']), 
                "r--", alpha=0.8, linewidth=2)
        
        figures['rating_vs_popularity'] = fig3
        
        return figures
    
    def print_summary(self):
        """
        Print a comprehensive summary of the dataset.
        """
        insights = self.get_basic_insights()
        
        if insights is None:
            print("❌ No data available. Please load the dataset first.")
            return
        
        print("\n" + "="*60)
        print("📊 MOVIE DATASET SUMMARY")
        print("="*60)
        
        print(f"\n📈 Basic Statistics:")
        print(f"   • Total Movies: {insights['total_movies']:,}")
        print(f"   • Total Ratings: {insights['total_ratings']:,}")
        print(f"   • Unique Users: {insights['unique_users']:,}")
        print(f"   • Average Rating: {insights['avg_rating']:.2f}")
        print(f"   • Rating Std Dev: {insights['rating_std']:.2f}")
        
        print(f"\n🏆 Top 5 Most Popular Movies:")
        for i, (_, row) in enumerate(insights['top_5_popular'].iterrows(), 1):
            print(f"   {i}. {row['title']} ({row['rating_count']} ratings, {row['avg_rating']:.2f} avg)")
        
        print(f"\n⭐ Top 5 Highest Rated Movies (min 10 ratings):")
        for i, (_, row) in enumerate(insights['top_5_rated'].iterrows(), 1):
            print(f"   {i}. {row['title']} ({row['avg_rating']:.2f} avg, {row['rating_count']} ratings)")
        
        print(f"\n🎭 Top 5 Genres:")
        top_genres = list(insights['genre_distribution'].items())[:5]
        for i, (genre, count) in enumerate(top_genres, 1):
            print(f"   {i}. {genre}: {count} movies")
        
        print("="*60)

# Example usage
if __name__ == "__main__":
    analyzer = MovieDataAnalyzer()
    analyzer.load_data()
    analyzer.print_summary()

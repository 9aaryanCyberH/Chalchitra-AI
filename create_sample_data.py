import pandas as pd
import numpy as np
import os

def create_sample_dataset():
    """Create sample movie and rating data for testing."""
    
    # Sample movies data
    sample_movies = [
        {"movieId": 1, "title": "The Dark Knight (2008)", "genres": "Action|Crime|Drama"},
        {"movieId": 2, "title": "Inception (2010)", "genres": "Action|Adventure|Sci-Fi"},
        {"movieId": 3, "title": "Pulp Fiction (1994)", "genres": "Crime|Drama"},
        {"movieId": 4, "title": "The Shawshank Redemption (1994)", "genres": "Drama"},
        {"movieId": 5, "title": "Fight Club (1999)", "genres": "Drama"},
        {"movieId": 6, "title": "Batman Begins (2005)", "genres": "Action|Adventure|Crime"},
        {"movieId": 7, "title": "The Matrix (1999)", "genres": "Action|Sci-Fi"},
        {"movieId": 8, "title": "Interstellar (2014)", "genres": "Adventure|Drama|Sci-Fi"},
        {"movieId": 9, "title": "The Godfather (1972)", "genres": "Crime|Drama"},
        {"movieId": 10, "title": "Forrest Gump (1994)", "genres": "Drama|Romance"},
        {"movieId": 11, "title": "The Silence of the Lambs (1991)", "genres": "Crime|Drama|Thriller"},
        {"movieId": 12, "title": "Goodfellas (1990)", "genres": "Crime|Drama"},
        {"movieId": 13, "title": "The Departed (2006)", "genres": "Crime|Drama|Thriller"},
        {"movieId": 14, "title": "The Prestige (2006)", "genres": "Drama|Mystery|Thriller"},
        {"movieId": 15, "title": "Memento (2000)", "genres": "Mystery|Thriller"},
        {"movieId": 16, "title": "The Usual Suspects (1995)", "genres": "Crime|Drama|Mystery"},
        {"movieId": 17, "title": "Se7en (1995)", "genres": "Crime|Drama|Mystery"},
        {"movieId": 18, "title": "The Green Mile (1999)", "genres": "Crime|Drama|Fantasy"},
        {"movieId": 19, "title": "Gladiator (2000)", "genres": "Action|Adventure|Drama"},
        {"movieId": 20, "title": "The Lion King (1994)", "genres": "Animation|Adventure|Drama"},
        {"movieId": 21, "title": "Titanic (1997)", "genres": "Drama|Romance"},
        {"movieId": 22, "title": "Avatar (2009)", "genres": "Action|Adventure|Fantasy"},
        {"movieId": 23, "title": "The Avengers (2012)", "genres": "Action|Adventure|Sci-Fi"},
        {"movieId": 24, "title": "Iron Man (2008)", "genres": "Action|Adventure|Sci-Fi"},
        {"movieId": 25, "title": "The Dark Knight Rises (2012)", "genres": "Action|Adventure|Crime"},
        {"movieId": 26, "title": "The Lord of the Rings: The Fellowship of the Ring (2001)", "genres": "Action|Adventure|Drama"},
        {"movieId": 27, "title": "The Lord of the Rings: The Two Towers (2002)", "genres": "Action|Adventure|Drama"},
        {"movieId": 28, "title": "The Lord of the Rings: The Return of the King (2003)", "genres": "Action|Adventure|Drama"},
        {"movieId": 29, "title": "Star Wars: Episode IV - A New Hope (1977)", "genres": "Action|Adventure|Fantasy"},
        {"movieId": 30, "title": "Star Wars: Episode V - The Empire Strikes Back (1980)", "genres": "Action|Adventure|Fantasy"},
        {"movieId": 31, "title": "Jurassic Park (1993)", "genres": "Action|Adventure|Sci-Fi"},
        {"movieId": 32, "title": "E.T. the Extra-Terrestrial (1982)", "genres": "Adventure|Family|Sci-Fi"},
        {"movieId": 33, "title": "Back to the Future (1985)", "genres": "Adventure|Comedy|Sci-Fi"},
        {"movieId": 34, "title": "The Terminator (1984)", "genres": "Action|Sci-Fi"},
        {"movieId": 35, "title": "Terminator 2: Judgment Day (1991)", "genres": "Action|Sci-Fi"},
        {"movieId": 36, "title": "Die Hard (1988)", "genres": "Action|Crime|Thriller"},
        {"movieId": 37, "title": "Indiana Jones and the Raiders of the Lost Ark (1981)", "genres": "Action|Adventure"},
        {"movieId": 38, "title": "Raiders of the Lost Ark (1981)", "genres": "Action|Adventure"},
        {"movieId": 39, "title": "Jaws (1975)", "genres": "Adventure|Drama|Thriller"},
        {"movieId": 40, "title": "The Exorcist (1973)", "genres": "Horror"},
        {"movieId": 41, "title": "The Shining (1980)", "genres": "Drama|Horror"},
        {"movieId": 42, "title": "A Clockwork Orange (1971)", "genres": "Crime|Drama|Sci-Fi"},
        {"movieId": 43, "title": "2001: A Space Odyssey (1968)", "genres": "Adventure|Sci-Fi"},
        {"movieId": 44, "title": "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1964)", "genres": "Comedy|War"},
        {"movieId": 45, "title": "Apocalypse Now (1979)", "genres": "Drama|War"},
        {"movieId": 46, "title": "The Good, the Bad and the Ugly (1966)", "genres": "Western"},
        {"movieId": 47, "title": "Once Upon a Time in the West (1968)", "genres": "Western"},
        {"movieId": 48, "title": "The Searchers (1956)", "genres": "Adventure|Drama|Western"},
        {"movieId": 49, "title": "Casablanca (1942)", "genres": "Drama|Romance|War"},
        {"movieId": 50, "title": "Gone with the Wind (1939)", "genres": "Drama|Romance|War"}
    ]
    
    movies_df = pd.DataFrame(sample_movies)
    
    # Generate sample ratings
    np.random.seed(42)  # For reproducible results
    ratings_data = []
    
    # Generate ratings for each movie
    for movie_id in range(1, 51):
        # Number of ratings for this movie (more popular movies get more ratings)
        n_ratings = np.random.poisson(50) + 10
        
        for _ in range(n_ratings):
            user_id = np.random.randint(1, 1001)  # 1000 users
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.15, 0.25, 0.3, 0.2])
            ratings_data.append({
                "userId": user_id,
                "movieId": movie_id,
                "rating": rating,
                "timestamp": np.random.randint(1000000000, 1600000000)
            })
    
    ratings_df = pd.DataFrame(ratings_data)
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Save to CSV files
    movies_df.to_csv("data/movies.csv", index=False)
    ratings_df.to_csv("data/ratings.csv", index=False)
    
    print("✅ Sample dataset created successfully!")
    print(f"📽️ Movies: {len(movies_df)}")
    print(f"⭐ Ratings: {len(ratings_df)}")
    print(f"👥 Users: {ratings_df['userId'].nunique()}")
    
    return movies_df, ratings_df

if __name__ == "__main__":
    create_sample_dataset()

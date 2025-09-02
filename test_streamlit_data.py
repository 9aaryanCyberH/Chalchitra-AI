#!/usr/bin/env python3
"""
Simple test script to verify data loading works in Streamlit deployment.
Run this with: streamlit run test_streamlit_data.py
"""

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Loading Test", page_icon="🔍")

st.title("🔍 Data Loading Test")
st.write("This page tests if the data files can be loaded in your Streamlit deployment.")

# Show current working directory
st.subheader("📁 Current Environment")
st.write(f"**Working Directory:** `{os.getcwd()}`")
st.write(f"**Script Location:** `{os.path.dirname(os.path.abspath(__file__))}`")

# List files in current directory
st.subheader("📋 Files in Current Directory")
try:
    files = os.listdir('.')
    file_list = []
    for file in files:
        if os.path.isfile(file):
            file_list.append(f"📄 {file}")
        else:
            file_list.append(f"📁 {file}/")
    st.write("\n".join(file_list))
except Exception as e:
    st.error(f"Error listing files: {e}")

# Check data directory
st.subheader("📁 Data Directory Check")
data_paths = ['data', './data', '../data']

for path in data_paths:
    if os.path.exists(path):
        st.success(f"✅ {path} exists")
        try:
            data_files = os.listdir(path)
            st.write(f"Files in {path}: {data_files}")
        except Exception as e:
            st.error(f"Error listing {path}: {e}")
    else:
        st.error(f"❌ {path} does not exist")

# Test data loading
st.subheader("📊 Data Loading Test")

# Test movies.csv
st.write("**🎬 Testing movies.csv loading:**")
movies_paths = ['data/movies.csv', './data/movies.csv', '../data/movies.csv', 'movies.csv']
movies_loaded = False

for path in movies_paths:
    if os.path.exists(path):
        st.success(f"Found movies.csv at: {path}")
        try:
            movies_df = pd.read_csv(path)
            st.success(f"✅ Successfully loaded movies.csv: {len(movies_df)} records")
            st.write(f"Columns: {list(movies_df.columns)}")
            st.dataframe(movies_df.head())
            movies_loaded = True
            break
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
    else:
        st.info(f"{path} does not exist")

# Test ratings.csv
st.write("**⭐ Testing ratings.csv loading:**")
ratings_paths = ['data/ratings.csv', './data/ratings.csv', '../data/ratings.csv', 'ratings.csv']
ratings_loaded = False

for path in ratings_paths:
    if os.path.exists(path):
        st.success(f"Found ratings.csv at: {path}")
        try:
            ratings_df = pd.read_csv(path)
            st.success(f"✅ Successfully loaded ratings.csv: {len(ratings_df)} records")
            st.write(f"Columns: {list(ratings_df.columns)}")
            st.dataframe(ratings_df.head())
            ratings_loaded = True
            break
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
    else:
        st.info(f"{path} does not exist")

# Summary
st.subheader("📊 Summary")
if movies_loaded and ratings_loaded:
    st.success("🎉 All data files loaded successfully! Your Streamlit app should work now.")
else:
    st.error("❌ Some data files failed to load. Check the paths above.")

# Test the MovieDataAnalyzer
st.subheader("🧠 Testing MovieDataAnalyzer")
try:
    from data_analysis import MovieDataAnalyzer
    
    analyzer = MovieDataAnalyzer()
    movies_df, ratings_df, movies_with_ratings = analyzer.load_data()
    
    if movies_df is not None and ratings_df is not None:
        st.success("✅ MovieDataAnalyzer.load_data() worked successfully!")
        st.write(f"Movies: {len(movies_df)} records")
        st.write(f"Ratings: {len(ratings_df)} records")
        st.write(f"Movies with ratings: {len(movies_with_ratings)} records")
    else:
        st.error("❌ MovieDataAnalyzer.load_data() failed!")
        
except Exception as e:
    st.error(f"Error testing MovieDataAnalyzer: {e}")
    st.write("This might indicate an import or path issue.")

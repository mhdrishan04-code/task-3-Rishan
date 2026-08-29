import os
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data():
    return pd.read_csv("movies.csv")


def fetch_real_poster(movie_title):
    # Free OMDb API key
    api_key = "b9a5e69d"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    try:
        response = requests.get(url, timeout=3).json()
        poster = response.get("Poster")
        if poster and poster != "N/A":
            return poster
    except Exception:
        pass

    # Fallback to styled placeholder if not found on OMDb
    title_clean = movie_title.replace(" ", "+")
    return f"https://placehold.co/300x450/1e293b/38bdf8?text={title_clean}"


def get_recommendations(genre, language, mood, top_n=5):
    data = load_data()

    # Combine movie features
    data["features"] = (
        data["genre"] + " " +
        data["language"] + " " +
        data["mood"]
    )

    # Convert text features into numerical vectors
    vectorizer = CountVectorizer()
    feature_vectors = vectorizer.fit_transform(data["features"])

    # Create user preference vector
    user_preferences = f"{genre} {language} {mood}"
    user_vector = vectorizer.transform([user_preferences])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        user_vector,
        feature_vectors
    ).flatten()

    data["similarity_score"] = similarity_scores

    # Sort top recommendations
    recommendations = data.sort_values(
        by="similarity_score",
        ascending=False
    ).head(top_n).copy()

    # Round similarity score
    recommendations["similarity_score"] = (
        recommendations["similarity_score"] * 100
    ).round(2)

    # Fetch exact poster dynamically
    recommendations["poster_url"] = recommendations["Title"].apply(fetch_real_poster)

    return recommendations[
        ["Title", "genre", "language", "mood", "poster_url", "similarity_score"]
    ]
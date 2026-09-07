import os
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data():
    return pd.read_csv("movies.csv")


def get_final_poster(row):
    # 1. Use direct image URL from movies.csv if present and not a placehold.co link
    csv_poster = str(row.get("poster_url", "")).strip()
    if csv_poster.startswith("http") and "placehold.co" not in csv_poster:
        return csv_poster

    # 2. Fall back to OMDb API if CSV does not have a direct poster
    movie_title = row.get("Title", "")
    api_key = "b9a5e69d"
    url = "https://www.omdbapi.com/"

    try:
        response = requests.get(
            url,
            params={"t": movie_title, "apikey": api_key},
            timeout=5
        )
        response.raise_for_status()
        result = response.json()
        poster = result.get("Poster")
        if poster and poster != "N/A":
            return poster
    except Exception:
        pass

    # 3. Final fallback placeholder
    title_clean = str(movie_title).replace(" ", "+")
    return f"https://placehold.co/300x450/1e293b/38bdf8?text={title_clean}"


def get_recommendations(genre, language, mood, top_n=5):
    data = load_data()

    data["features"] = (
        data["genre"].fillna("").astype(str) + " " +
        data["language"].fillna("").astype(str) + " " +
        data["mood"].fillna("").astype(str)
    )

    vectorizer = CountVectorizer()
    feature_vectors = vectorizer.fit_transform(data["features"])

    user_preferences = f"{genre} {language} {mood}"
    user_vector = vectorizer.transform([user_preferences])

    similarity_scores = cosine_similarity(
        user_vector,
        feature_vectors
    ).flatten()

    data["similarity_score"] = similarity_scores

    recommendations = data.sort_values(
        by="similarity_score",
        ascending=False
    ).head(top_n).copy()

    recommendations["similarity_score"] = (
        recommendations["similarity_score"] * 100
    ).round(2)

    # Prioritize CSV poster links
    recommendations["poster_url"] = recommendations.apply(get_final_poster, axis=1)

    return recommendations[
        ["Title", "genre", "language", "mood", "poster_url", "similarity_score"]
    ]

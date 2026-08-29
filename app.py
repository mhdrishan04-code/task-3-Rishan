import os
import streamlit as st
from PIL import Image

# Import get_recommendations (wrapped in try-except for robustness)
try:
    from recommender import get_recommendations
except ImportError:
    st.error("Could not import 'get_recommendations' from 'recommender.py'. Ensure the file exists.")
    st.stop()

# --- PAGE CONFIGURATION & LOGO SETUP ---
LOGO_PATH = "logo.png"
has_logo = os.path.exists(LOGO_PATH)
logo_img = Image.open(LOGO_PATH) if has_logo else None

st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon=logo_img if has_logo else "🎬",
    layout="centered"
)

if has_logo:
    st.image(logo_img, width=150)

# --- MOBILE FRIENDLY UI & CUSTOM STYLES ---
st.markdown("""
<style>
.stApp {
    background-color: #0e0e0e;
    color: white;
}
h1 {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
}
.movie-card {
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #333;
    margin-bottom: 18px;
    background-color: #171717;
}
.movie-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 8px;
}
.movie-info {
    font-size: 16px;
    line-height: 1.8;
}
.similarity {
    font-size: 16px;
    font-weight: bold;
    margin-top: 10px;
    padding: 6px 12px;
    border-radius: 8px;
    background-color: #252525;
    display: inline-block;
}
@media (max-width: 600px) {
    h1 { font-size: 28px; }
    .movie-title { font-size: 20px; }
    .movie-info { font-size: 14px; }
    .similarity { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("AI Movie Recommendation System")
st.write("Find movies that match your taste!")

# --- DEFINE CONSTANTS FOR OPTIONS & DEFAULTS ---
GENRE_OPTIONS = ["Sci-Fi", "Comedy", "Sports", "Thriller", "Romance", "Drama", "Action", "Adventure", "Fantasy", "Mystery", "Crime"]
LANGUAGE_OPTIONS = ["English", "Hindi", "Malayalam", "Tamil", "Telugu", "Kannada", "Japanese", "Korean", "Spanish", "Italian", "Chinese"]
MOOD_OPTIONS = ["Emotional", "Thriller", "Inspirational", "Adventure", "Suspense", "Feel Good", "Dark", "Spiritual", "Action"]

DEFAULT_GENRE = GENRE_OPTIONS[0]
DEFAULT_LANGUAGE = LANGUAGE_OPTIONS[0]
DEFAULT_MOOD = MOOD_OPTIONS[0]
DEFAULT_SEARCH = ""

# --- INITIALIZE SESSION STATE (The Fix) ---
if 'genre_select' not in st.session_state:
    st.session_state['genre_select'] = DEFAULT_GENRE
if 'language_select' not in st.session_state:
    st.session_state['language_select'] = DEFAULT_LANGUAGE
if 'mood_select' not in st.session_state:
    st.session_state['mood_select'] = DEFAULT_MOOD
if 'search_input' not in st.session_state:
    st.session_state['search_input'] = DEFAULT_SEARCH

# --- USER INPUTS (Now tied to initialized Session State) ---
genre = st.selectbox(
    "🎭 Select Genre",
    GENRE_OPTIONS,
    key="genre_select"
)

language = st.selectbox(
    "🌐 Select Language",
    LANGUAGE_OPTIONS,
    key="language_select"
)

mood = st.selectbox(
    "😊 Select Mood",
    MOOD_OPTIONS,
    key="mood_select"
)

search_movie = st.text_input(
    "🔍 Search Movie",
    placeholder="Enter movie name...",
    key="search_input"
).strip()

# --- ACTION BUTTONS (GET RECOMMENDATIONS & RESET) ---
col_btn1, col_btn2 = st.columns([2, 1])

with col_btn1:
    get_rec_clicked = st.button("🔍 Get Recommendations", type="primary", use_container_width=True)

with col_btn2:
    if st.button("🔄 Clear / Reset", use_container_width=True):
        # Delete keys to reset widgets to initial values
        del st.session_state["genre_select"]
        del st.session_state["language_select"]
        del st.session_state["mood_select"]
        del st.session_state["search_input"]
        st.rerun()

# --- RECOMMENDATION DISPLAY ---
if get_rec_clicked:
    # Double-check recommendations function exists before running
    if 'get_recommendations' not in globals():
        st.error("Recommendation engine is not loaded.")
    else:
        with st.spinner("Finding recommendations..."):
            # Ensure input values aren't somehow None, use defaults if they are
            current_genre = genre if genre else DEFAULT_GENRE
            current_language = language if language else DEFAULT_LANGUAGE
            current_mood = mood if mood else DEFAULT_MOOD
            
            recommendations = get_recommendations(current_genre, current_language, current_mood)

        st.subheader("⭐ Recommended Movies")

        if recommendations is not None and not recommendations.empty:
            title_col = "title" if "title" in recommendations.columns else "Title"

            # Filter by search term if provided
            if search_movie:
                recommendations = recommendations[
                    recommendations[title_col].astype(str).str.contains(
                        search_movie,
                        case=False,
                        na=False
                    )
                ]

            # Display results
            if search_movie and recommendations.empty:
                st.warning(f"🎬 No movie found matching '{search_movie}'.")
            elif recommendations.empty:
                st.warning("No recommendations found for the selected criteria.")
            else:
                for _, movie in recommendations.iterrows():
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 2.5])

                    with col1:
                        poster = movie.get("poster_url")
                        if poster and isinstance(poster, str) and poster.strip():
                            st.image(poster, width=130)
                        else:
                            st.write("🎬 No Poster")

                    with col2:
                        movie_title = movie.get(title_col, "Unknown")
                        st.markdown(f'<div class="movie-title">🎬 {movie_title}</div>', unsafe_allow_html=True)

                        st.markdown(
                            f"""
                            <div class="movie-info">
                            🎭 <b>Genre:</b> {movie.get('genre', 'N/A')}<br>
                            🌐 <b>Language:</b> {movie.get('language', 'N/A')}<br>
                            😊 <b>Mood:</b> {movie.get('mood', 'N/A')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        sim_score = movie.get("similarity_score", "N/A")
                        st.markdown(
                            f"""
                            <div class="similarity">
                            ⭐ Match Score: {sim_score}%
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No recommendations found for the selected criteria.")

# --- ABOUT PROJECT ---
st.markdown("---")

with st.expander("ℹ️ About This Project"):
    st.markdown("""
    ### 🎬 AI Movie Recommendation System

    This project recommends movies based on:
    * 🎭 Genre
    * 🌐 Language
    * 😊 Mood

    ### 🤖 How It Works
    The system analyzes the selected movie preferences and calculates a similarity score to recommend the most relevant movies.

    ### 🛠️ Technologies Used
    * 🐍 Python
    * 🎈 Streamlit
    * 📊 Pandas
    * 🤖 Machine Learning
    * 🎬 Movie Dataset

    **Developed as an AI/ML academic project.**
    """)
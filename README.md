# 🎬 AI Movie Recommendation System

A content-based movie recommendation web application built with Streamlit, Scikit-learn, and Pandas. The app recommends films tailored to user preferences across genre, language, and mood using text vectorization and cosine similarity.

---test this app 

## 📌 Features

* **Multi-Attribute Filtering:** Filter movie suggestions based on Genre, Language, and Mood.
* **Content-Based Recommendation:** Uses `CountVectorizer` and `cosine_similarity` to calculate match scores.
* **Real-time Search:** Filter recommended titles by keyword/title substring.
* **Dynamic Poster Rendering:** Direct poster image integration with fallback support via OMDb API and image placeholders.
* **Responsive Dark UI:** Streamlit interface customized with styled cards and match percentage indicators.

---

## 🛠️ Tech Stack

* **Frontend / Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Machine Learning:** [Scikit-learn](https://scikit-learn.org/) (`CountVectorizer`, `cosine_similarity`)
* **Image & Network Handling:** `Pillow`, `Requests`

---

## 📂 Project Structure

```text
├── app.py              # Main Streamlit web application
├── recommender.py      # Recommendation engine & poster resolution logic
├── movies.csv          # Movie dataset (Title, genre, language, mood, poster_url)
├── requirements.txt    # Project dependencies
├── logo.png            # Application logo (optional)
└── README.md           # Project documentation

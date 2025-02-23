import streamlit as st
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download nltk data
nltk.download("punkt")

# Load dataset
file_path = "Seven_Sisters_Travel_Packages.csv"
df = pd.read_csv(file_path)

# Ensure required columns exist
expected_columns = ["State", "Weather", "Activities", "Cultural Highlights", "Budget Level", "Budget (INR)"]
for col in expected_columns:
    if col not in df.columns:
        st.error(f"Missing column: {col} in dataset.")
        st.stop()

# Preprocess travel packages
df["Processed"] = df["State"].fillna("") + " " + df["Weather"].fillna("") + " " + df["Activities"].fillna("") + " " + df["Cultural Highlights"].fillna("")

# Train a TF-IDF model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Processed"])

def get_best_match(query):
    """Find the best travel package based on user query."""
    words = query.lower().split()
    
    # Check if the user is asking for a specific state
    for word in words:
        capitalized_word = word.capitalize()
        if capitalized_word in df["State"].values:
            matches = df[df["State"] == capitalized_word]
            if not matches.empty:
                return matches
            else:
                return None

    # If no exact state match, use TF-IDF similarity
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    best_index = similarities.argmax()
    if similarities[best_index] > 0.1:
        return df.iloc[[best_index]]  # Return as DataFrame to handle multiple results
    else:
        return None

# Streamlit UI
st.title("🌍 Explore Northeast India: Travel Chatbot")
st.write("Discover the best travel experiences in the Seven Sisters of India!")

# Quick question buttons
st.subheader("Quick Questions:")
col1, col2, col3 = st.columns(3)
if col1.button("Best package for adventure?"):
    query = "adventure"
elif col2.button("Budget-friendly tours?"):
    query = "budget"
elif col3.button("Cultural experiences?"):
    query = "culture"
else:
    query = st.text_input("You: ")

if query:
    result = get_best_match(query)
    
    if result is not None and not result.empty:
        st.subheader("🎯 Recommended Packages")
        for _, row in result.iterrows():  # Iterate through multiple results
            st.write(f"**State:** {row['State']}")
            st.write(f"**Weather:** {row['Weather']}")
            st.write(f"**Activities:** {row['Activities']}")
            st.write(f"**Cultural Highlights:** {row['Cultural Highlights']}")
            st.write(f"**Budget Level:** {row['Budget Level']}")
            st.write(f"**Budget (INR):** {row['Budget (INR)']}")
            st.markdown("---")  # Add separator
    else:
        st.write("🤖 Sorry, no relevant packages found.")

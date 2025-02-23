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

# Check required columns
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

def get_best_matches(query, num_results=3):
    """Finds the top travel packages based on user query."""
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    sorted_indices = similarities.argsort()[::-1]  # Sort in descending order
    top_indices = [idx for idx in sorted_indices if similarities[idx] > 0.1][:num_results]

    return df.iloc[top_indices] if top_indices else None

def handle_general_queries(query):
    """Handles greetings and state-specific package requests."""
    greetings = ["hi", "hello", "hey"]
    if query.lower() in greetings:
        return "👋 Hello! How can I assist you with travel recommendations?"

    # Check if user is asking for packages for a specific state
    words = query.lower().split()
    for word in words:
        capitalized_word = word.capitalize()
        if capitalized_word in df["State"].values:
            matches = df[df["State"] == capitalized_word]
            return matches if not matches.empty else "I couldn't find specific packages for that location."

    return None  # Proceed to TF-IDF matching

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
    general_response = handle_general_queries(query)

    if general_response:
        if isinstance(general_response, str):  # If it's a text response (e.g., greetings)
            st.write(general_response)
        else:  # If it's a dataframe with package suggestions
            st.subheader("🌍 Suggested Travel Packages")
            for _, row in general_response.iterrows():
                st.write(f"**State:** {row['State']}")
                st.write(f"**Weather:** {row['Weather']}")
                st.write(f"**Activities:** {row['Activities']}")
                st.write(f"**Cultural Highlights:** {row['Cultural Highlights']}")
                st.write(f"**Budget Level:** {row['Budget Level']}")
                st.write(f"**Budget (INR):** {row['Budget (INR)']}")
                st.write("---")
    else:
        results = get_best_matches(query)
        if results is not None:
            st.subheader("🎯 Recommended Travel Packages")
            for _, row in results.iterrows():
                st.write(f"**State:** {row['State']}")
                st.write(f"**Weather:** {row['Weather']}")
                st.write(f"**Activities:** {row['Activities']}")
                st.write(f"**Cultural Highlights:** {row['Cultural Highlights']}")
                st.write(f"**Budget Level:** {row['Budget Level']}")
                st.write(f"**Budget (INR):** {row['Budget (INR)']}")
                st.write("---")
        else:
            st.write("🤖 Sorry, I couldn't find relevant travel packages.")

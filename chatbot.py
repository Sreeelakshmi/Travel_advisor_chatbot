import streamlit as st
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download nltk data
nltk.download("punkt")

# Load dataset
df = pd.read_csv("Seven_Sisters_Travel_Packages.csv")

# Preprocess travel packages
df["Processed"] = df["State"].fillna("") + " " + df["Weather"].fillna("") + " " + df["Activities"].fillna("") + " " + df["Cultural Highlights"].fillna("")

# Train a TF-IDF model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Processed"])

def get_best_match(query):
    """Find the best travel package based on user query."""
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    best_index = similarities.argmax()
    if similarities[best_index] > 0.1:
        return df.iloc[best_index]
    else:
        return None

# Streamlit UI
st.title("🌍 Northeast India Travel Guide Chatbot")
st.write("Explore the best travel options across the Seven Sisters states!")

# Quick question buttons
st.subheader("Quick Questions:")
col1, col2, col3 = st.columns(3)
if col1.button("Best adventure spots?"):
    query = "adventure"
elif col2.button("Budget-friendly trips?"):
    query = "budget"
elif col3.button("Cultural experiences?"):
    query = "culture"
else:
    query = st.text_input("You: ")

if query:
    result = get_best_match(query)
    
    if result is not None:
        st.subheader("🎯 Recommended Travel Destination")
        st.write(f"**State:** {result['State']}")
        st.write(f"**Weather:** {result['Weather']}")
        st.write(f"**Activities:** {result['Activities']}")
        st.write(f"**Cultural Highlights:** {result['Cultural Highlights']}")
        st.write(f"**Budget Level:** {result['Budget Level']}")
        st.write(f"**Budget (INR):** {result['Budget (INR)']}")
        
        # Show image if available
        if 'Image_URL' in result and pd.notna(result['Image_URL']):
            st.image(result['Image_URL'], caption=result['State'], use_column_width=True)
    else:
        st.write("🤖 Sorry, no relevant travel options found.")

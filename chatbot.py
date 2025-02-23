import streamlit as st
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("Seven_Sisters_Travel_Packages.csv")

# Preprocess travel packages
nltk.download("punkt")
df["Processed"] = df["Destination"].fillna("") + " " + df["Description"].fillna("")

# Train a TF-IDF model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Processed"])

def get_best_match(query):
    """Find the best travel package based on user query."""
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    best_index = similarities.argmax()
    if similarities[best_index] > 0.1:
        return df.iloc[best_index].to_dict()
    else:
        return "Sorry, no relevant packages found."

# Streamlit UI
st.title("🗺️ Seven Sisters Travel Chatbot")
st.write("Ask about travel packages in Northeast India!")

query = st.text_input("You: ")

if query:
    response = get_best_match(query)
    st.write(f"🤖 Chatbot: {response}")

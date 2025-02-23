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
df["Processed"] = (
    df["State"].fillna("") + " " +
    df["Weather"].fillna("") + " " +
    df["Activities"].fillna("") + " " +
    df["Cultural Highlights"].fillna("")
)

# Train a TF-IDF model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Processed"])

def get_best_match(query, budget=None, transport=None, family_friendly=None):
    """Find the best travel package based on user query and filters."""
    filtered_df = df.copy()
    
    if budget:
        filtered_df = filtered_df[filtered_df["Budget Level"].str.lower() == budget.lower()]
    if transport:
        filtered_df = filtered_df[filtered_df["Transportation Options"].str.contains(transport, case=False, na=False)]
    if family_friendly:
        filtered_df = filtered_df[filtered_df["Family-Friendly"].str.lower() == family_friendly.lower()]
    
    if filtered_df.empty:
        return None
    
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, vectorizer.transform(filtered_df["Processed"])).flatten()
    
    best_index = similarities.argmax()
    if similarities[best_index] > 0.1:
        return filtered_df.iloc[best_index]
    else:
        return None

# Streamlit UI
st.title("🌍 Explore Northeast India: Travel Chatbot")
st.write("Discover the best travel experiences in the Seven Sisters of India!")

# User Inputs
query = st.text_input("What are you looking for?")
budget = st.selectbox("Select Budget Level", ["Any", "Low", "Medium", "High"])
transport = st.selectbox("Preferred Mode of Transport", ["Any", "Car", "Bus", "Train", "Flight"])
family_friendly = st.radio("Family-Friendly?", ["Any", "Yes", "No"])

# Convert 'Any' to None
def convert_none(value):
    return None if value == "Any" else value

budget = convert_none(budget)
transport = convert_none(transport)
family_friendly = convert_none(family_friendly)

if query:
    result = get_best_match(query, budget, transport, family_friendly)
    
    if result is not None:
        st.subheader("🎯 Recommended Package")
        st.write(f"**State:** {result['State']}")
        st.write(f"**Weather:** {result['Weather']}")
        st.write(f"**Activities:** {result['Activities']}")
        st.write(f"**Cultural Highlights:** {result['Cultural Highlights']}")
        st.write(f"**Budget Level:** {result['Budget Level']}")
        st.write(f"**Budget (INR):** {result['Budget (INR)']}")
        st.write(f"**Transportation Options:** {result['Transportation Options']}")
        st.write(f"**Family-Friendly:** {result['Family-Friendly']}")
    else:
        st.write("🤖 Sorry, no relevant packages found.")

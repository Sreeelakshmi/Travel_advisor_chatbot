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
        return df.iloc[best_index]
    else:
        return None

# Streamlit UI
st.title("\U0001F30D Seven Sisters Travel Chatbot")
st.write("Ask about travel packages in Northeast India!")

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
    
    if result is not None:
        st.subheader("\U0001F3AF Recommended Package")
        st.write(f"**Destination:** {result['Destination']}")
        st.write(f"**Description:** {result['Description']}")
        st.write(f"**Price:** {result['Price']}")
        
        # Show image if available
        if 'Image_URL' in result and pd.notna(result['Image_URL']):
            st.image(result['Image_URL'], caption=result['Destination'], use_column_width=True)
    else:
        st.write("\U0001F916 Sorry, no relevant packages found.")

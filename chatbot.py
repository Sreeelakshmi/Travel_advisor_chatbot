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
st.write("Hello! I'm your travel assistant. How can I help you today?")

# Chatbot-style interaction
if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You:")

if user_input:
    st.session_state.conversation.append(f"You: {user_input}")
    
    if "package" in user_input.lower():
        st.write("Let's find the perfect package for you! Answer a few questions:")
        budget = st.selectbox("Select Budget Level", ["Any", "Low", "Medium", "High"])
        transport = st.selectbox("Preferred Mode of Transport", ["Any", "Car", "Bus", "Train", "Flight"])
        family_friendly = st.radio("Family-Friendly?", ["Any", "Yes", "No"])
        
        # Convert 'Any' to None
        def convert_none(value):
            return None if value == "Any" else value
        
        budget = convert_none(budget)
        transport = convert_none(transport)
        family_friendly = convert_none(family_friendly)
        
        result = get_best_match(user_input, budget, transport, family_friendly)
        
        if result is not None:
            response = (f"🎯 Recommended Package:\n"
                        f"**State:** {result['State']}\n"
                        f"**Weather:** {result['Weather']}\n"
                        f"**Activities:** {result['Activities']}\n"
                        f"**Cultural Highlights:** {result['Cultural Highlights']}\n"
                        f"**Budget Level:** {result['Budget Level']}\n"
                        f"**Budget (INR):** {result['Budget (INR)']}\n"
                        f"**Transportation Options:** {result['Transportation Options']}\n"
                        f"**Family-Friendly:** {result['Family-Friendly']}")
        else:
            response = "🤖 Sorry, no relevant packages found."
    else:
        response = "I'm here to help! Ask me about travel packages, destinations, or activities."
    
    st.session_state.conversation.append(f"Bot: {response}")

# Display conversation history
for message in st.session_state.conversation:
    st.write(message)

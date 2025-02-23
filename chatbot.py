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

def process_input(user_input):
    if "package" in user_input.lower():
        result = get_best_match(user_input)
        if result is not None:
            return (f"🎯 **Recommended Package:**\n"
                    f"**State:** {result['State']}\n"
                    f"**Weather:** {result['Weather']}\n"
                    f"**Activities:** {result['Activities']}\n"
                    f"**Cultural Highlights:** {result['Cultural Highlights']}\n"
                    f"**Budget Level:** {result['Budget Level']}\n"
                    f"**Budget (INR):** {result['Budget (INR)']}\n"
                    f"**Transportation Options:** {result['Transportation Options']}\n"
                    f"**Family-Friendly:** {result['Family-Friendly']}")
        else:
            return "🤖 Sorry, no relevant packages found."
    elif "location" in user_input.lower():
        locations = df["State"].unique()
        return "📍 **Available Locations:** " + ", ".join(locations)
    elif "best place to visit" in user_input.lower():
        best_places = df.sort_values(by="Budget (INR)", ascending=False)["State"].unique()[:5]
        return "🌟 **Best Places to Visit:** " + ", ".join(best_places)
    elif "weather" in user_input.lower():
        weather_info = df.groupby("State")["Weather"].first().to_dict()
        return "☁️ **Weather Information:**\n" + "\n".join([f"{state}: {weather}" for state, weather in weather_info.items()])
    else:
        return "🤖 I'm here to help! Ask me about travel packages, destinations, or activities."

# Display conversation history above input field
for message in st.session_state.conversation:
    st.write(message)

# User input field
user_input = st.text_input("You:", "", key="user_input")

if user_input:
    st.session_state.conversation.append(f"You: {user_input}")
    response = process_input(user_input)
    st.session_state.conversation.append(f"Bot: {response}")
    
    # Clear input field after response
    st.rerun()

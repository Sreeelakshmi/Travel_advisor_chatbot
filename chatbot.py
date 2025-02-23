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

st.write("### Choose a topic to explore:")
option = st.radio("Select an option:", ["Travel Packages", "Locations", "Best Places to Visit", "Weather Information"])

if option == "Travel Packages":
    st.write("🛫 Do you have any preferences?")
    budget = st.selectbox("Budget Level:", ["Low", "Medium", "High", "Any"], index=3)
    transport = st.text_input("Preferred Transport (e.g., Car, Train, Flight):")
    family_friendly = st.radio("Family-Friendly:", ["Yes", "No", "Any"], index=2)
    
    if st.button("Find Package"):
        budget = None if budget == "Any" else budget
        family_friendly = None if family_friendly == "Any" else family_friendly
        result = get_best_match("travel package", budget, transport, family_friendly)
        
        if result is not None:
            st.write(f"🎯 **Recommended Package:**\n"
                     f"**State:** {result['State']}\n"
                     f"**Weather:** {result['Weather']}\n"
                     f"**Activities:** {result['Activities']}\n"
                     f"**Cultural Highlights:** {result['Cultural Highlights']}\n"
                     f"**Budget Level:** {result['Budget Level']}\n"
                     f"**Budget (INR):** {result['Budget (INR)']}\n"
                     f"**Transportation Options:** {result['Transportation Options']}\n"
                     f"**Family-Friendly:** {result['Family-Friendly']}")
        else:
            st.write("🤖 Sorry, no relevant packages found.")

elif option == "Locations":
    locations = df["State"].unique()
    st.write("📍 **Available Locations:** " + ", ".join(locations))

elif option == "Best Places to Visit":
    best_places = df.sort_values(by="Budget (INR)", ascending=False)["State"].unique()[:5]
    st.write("🌟 **Best Places to Visit:** " + ", ".join(best_places))

elif option == "Weather Information":
    weather_info = df.groupby("State")["Weather"].first().to_dict()
    st.write("☁️ **Weather Information:**\n" + "\n".join([f"{state}: {weather}" for state, weather in weather_info.items()]))

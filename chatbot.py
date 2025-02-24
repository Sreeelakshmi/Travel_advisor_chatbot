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
option = st.radio("Select an option:", ["Travel Packages", "Locations", "Best Places to Visit", "Weather Information", "Local Cuisine", "Adventure Activities", "Festivals & Events"])

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
    state = st.selectbox("Select a state:", df["State"].unique())
    best_places = df[df["State"] == state]["Activities"].explode().dropna().unique()
    if best_places.size > 0:
        st.write(f"🌟 **Best Places to Visit in {state}:** " + ", ".join(best_places))
    else:
        st.write(f"🤖 No specific recommendations available for {state}.")

elif option == "Weather Information":
    weather_info = df.groupby("State")["Weather"].first().to_dict()
    for state, weather in weather_info.items():
        st.write(f"☁️ **{state}:** {weather}")

elif option == "Local Cuisine":
    state = st.selectbox("Select a state:", df["State"].unique())
    cuisines = df[df["State"] == state]["Cuisines"].dropna().unique()
    if cuisines.size > 0:
        st.write(f"🍽️ **Famous Cuisines in {state}:** " + ", ".join(cuisines))
    else:
        st.write(f"🤖 No cuisine data available for {state}.")

elif option == "Adventure Activities":
    activity = st.text_input("Enter an adventure activity (e.g., Trekking, Rafting, Paragliding):")
    states_with_activity = df[df["Activities"].str.contains(activity, case=False, na=False)]["State"].unique()
    if states_with_activity.size > 0:
        st.write(f"🎢 **States offering {activity}:** " + ", ".join(states_with_activity))
    else:
        st.write(f"🤖 No states found for {activity}.")

elif option == "Festivals & Events":
    state = st.selectbox("Select a state:", df["State"].unique())
    festivals = df[df["State"] == state]["Cultural Highlights"].dropna().unique()
    if festivals.size > 0:
        st.write(f"🎉 **Major Festivals in {state}:** " + ", ".join(festivals))
    else:
        st.write(f"🤖 No festival data available for {state}.")

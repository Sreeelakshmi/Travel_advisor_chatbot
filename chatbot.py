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
st.write("Hello! I'm your travel assistant. Ask me anything about travel packages, locations, activities, and more!")

# Chatbot-style interaction
if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You: ", "")

if user_input:
    st.session_state.conversation.append(f"You: {user_input}")
    
    # Simple intent recognition
    if "package" in user_input.lower():
        budget = None
        transport = None
        family_friendly = None
        
        # Extract budget, transport, and family-friendly info from user input
        if "low" in user_input.lower():
            budget = "Low"
        elif "medium" in user_input.lower():
            budget = "Medium"
        elif "high" in user_input.lower():
            budget = "High"
        
        if "car" in user_input.lower():
            transport = "Car"
        elif "train" in user_input.lower():
            transport = "Train"
        elif "flight" in user_input.lower():
            transport = "Flight"
        
        if "family" in user_input.lower() and "friendly" in user_input.lower():
            family_friendly = "Yes"
        elif "not family" in user_input.lower():
            family_friendly = "No"
        
        result = get_best_match("travel package", budget, transport, family_friendly)
        
        if result is not None:
            response = (f"🎯 **Recommended Package:**\n"
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
    
    elif "locations" in user_input.lower():
        locations = df["State"].unique()
        response = "📍 **Available Locations:** " + ", ".join(locations)
    
    elif "best places" in user_input.lower():
        state = user_input.split("in")[-1].strip() if "in" in user_input else None
        if state and state in df["State"].values:
            best_places = df[df["State"] == state]["Activities"].explode().dropna().unique()
            if best_places.size > 0:
                response = f"🌟 **Best Places to Visit in {state}:** " + ", ".join(best_places)
            else:
                response = f"🤖 No specific recommendations available for {state}."
        else:
            response = "🤖 Please specify a valid state."
    
    elif "weather" in user_input.lower():
        weather_info = df.groupby("State")["Weather"].first().to_dict()
        response = "\n".join([f"☁️ **{state}:** {weather}" for state, weather in weather_info.items()])
    
    elif "cuisine" in user_input.lower():
        state = user_input.split("in")[-1].strip() if "in" in user_input else None
        if state and state in df["State"].values:
            cuisines = df[df["State"] == state]["Cuisines"].dropna().unique()
            if cuisines.size > 0:
                response = f"🍽️ **Famous Cuisines in {state}:** " + ", ".join(cuisines)
            else:
                response = f"🤖 No cuisine data available for {state}."
        else:
            response = "🤖 Please specify a valid state."
    
    elif "adventure" in user_input.lower():
        activity = user_input.split("activity")[-1].strip() if "activity" in user_input else None
        if activity:
            states_with_activity = df[df["Activities"].str.contains(activity, case=False, na=False)]["State"].unique()
            if states_with_activity.size > 0:
                response = f"🎢 **States offering {activity}:** " + ", ".join(states_with_activity)
            else:
                response = f"🤖 No states found for {activity}."
        else:
            response = "🤖 Please specify an adventure activity."
    
    elif "festival" in user_input.lower():
        state = user_input.split("in")[-1].strip() if "in" in user_input else None
        if state and state in df["State"].values:
            festivals = df[df["State"] == state]["Cultural Highlights"].dropna().unique()
            if festivals.size > 0:
                response = f"🎉 **Major Festivals in {state}:** " + ", ".join(festivals)
            else:
                response = f"🤖 No festival data available for {state}."
        else:
            response = "🤖 Please specify a valid state."
    
    else:
        response = "🤖 I'm sorry, I didn't understand that. Can you ask something else?"
    
    st.session_state.conversation.append(f"Bot: {response}")

# Display conversation
for message in st.session_state.conversation:
    st.write(message)

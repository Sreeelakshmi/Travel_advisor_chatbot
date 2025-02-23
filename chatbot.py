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
st.write("Hello! I'm your travel assistant. How can I help you today? Type your query below.")

# Chatbot-style interaction
if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_query = st.text_input("Your question:")
if user_query:
    st.session_state.conversation.append(f"🧑‍💻 You: {user_query}")
    
    # Process query
    result = get_best_match(user_query)
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
        response = "🤖 Sorry, I couldn't find a relevant package. Try specifying your preferences more clearly."
    
    st.session_state.conversation.append(f"🤖 Bot: {response}")

# Display conversation history
for message in st.session_state.conversation:
    st.write(message)

# Optional selections for refinement
st.write("### Refine your search:")
budget = st.selectbox("Budget Level:", ["Low", "Medium", "High", "Any"], index=3)
transport = st.text_input("Preferred Transport (e.g., Car, Train, Flight):")
family_friendly = st.radio("Family-Friendly:", ["Yes", "No", "Any"], index=2)

if st.button("Refine Search"):
    budget = None if budget == "Any" else budget
    family_friendly = None if family_friendly == "Any" else family_friendly
    refined_result = get_best_match(user_query, budget, transport, family_friendly)
    
    if refined_result is not None:
        refined_response = (f"🎯 **Refined Package:**\n"
                            f"**State:** {refined_result['State']}\n"
                            f"**Weather:** {refined_result['Weather']}\n"
                            f"**Activities:** {refined_result['Activities']}\n"
                            f"**Cultural Highlights:** {refined_result['Cultural Highlights']}\n"
                            f"**Budget Level:** {refined_result['Budget Level']}\n"
                            f"**Budget (INR):** {refined_result['Budget (INR)']}\n"
                            f"**Transportation Options:** {refined_result['Transportation Options']}\n"
                            f"**Family-Friendly:** {refined_result['Family-Friendly']}")
    else:
        refined_response = "🤖 Sorry, no relevant packages found with these filters."
    
    st.session_state.conversation.append(f"🤖 Bot: {refined_response}")

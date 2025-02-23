import streamlit as st
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download nltk data
nltk.download("punkt")

# Load dataset
file_path = "Seven_Sisters_Travel_Packages.csv"
df = pd.read_csv(file_path)

# Ensure required columns exist
expected_columns = ["State", "Weather", "Activities", "Cultural Highlights", "Budget Level", "Budget (INR)", "Family Friendly", "Transportation"]
for col in expected_columns:
    if col not in df.columns:
        st.error(f"Missing column: {col} in dataset.")
        st.stop()

# Preprocess travel packages
df["Processed"] = df["State"].fillna("") + " " + df["Weather"].fillna("") + " " + df["Activities"].fillna("") + " " + df["Cultural Highlights"].fillna("")

# Train a TF-IDF model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Processed"])

def get_filtered_packages(state, budget, family_friendly, transport):
    """Filter packages based on user preferences."""
    filtered_df = df[df["State"] == state]

    if budget:
        filtered_df = filtered_df[filtered_df["Budget Level"].str.lower() == budget.lower()]

    if family_friendly is not None:
        filtered_df = filtered_df[filtered_df["Family Friendly"].astype(str).str.lower() == str(family_friendly).lower()]

    if transport:
        filtered_df = filtered_df[filtered_df["Transportation"].str.lower().str.contains(transport.lower(), na=False)]

    return filtered_df

# Streamlit UI
st.title("🌍 Explore Northeast India: Travel Chatbot")
st.write("Discover the best travel experiences in the Seven Sisters of India!")

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
    words = query.lower().split()
    selected_state = None

    # Identify if user mentioned a state
    for word in words:
        capitalized_word = word.capitalize()
        if capitalized_word in df["State"].unique():
            selected_state = capitalized_word
            break

    if selected_state:
        st.subheader(f"🔍 Filtering Packages in {selected_state}")
        
        # Ask filtering questions
        budget = st.selectbox("Select your budget:", ["Any", "Low", "Medium", "High"])
        family_friendly = st.radio("Is this trip family-friendly?", ["Any", "Yes", "No"])
        transport = st.selectbox("Preferred mode of transport:", ["Any", "Car", "Bus", "Train", "Flight"])

        # Convert "Any" to None
        budget = None if budget == "Any" else budget
        family_friendly = None if family_friendly == "Any" else (family_friendly == "Yes")
        transport = None if transport == "Any" else transport

        # Get filtered results
        result = get_filtered_packages(selected_state, budget, family_friendly, transport)

        if not result.empty:
            st.subheader("🎯 Recommended Packages")
            for _, row in result.iterrows():  # Iterate through multiple results
                st.write(f"**State:** {row['State']}")
                st.write(f"**Weather:** {row['Weather']}")
                st.write(f"**Activities:** {row['Activities']}")
                st.write(f"**Cultural Highlights:** {row['Cultural Highlights']}")
                st.write(f"**Budget Level:** {row['Budget Level']}")
                st.write(f"**Budget (INR):** {row['Budget (INR)']}")
                st.write(f"**Family Friendly:** {row['Family Friendly']}")
                st.write(f"**Transportation:** {row['Transportation']}")
                st.markdown("---")  # Add separator
        else:
            st.write(f"🤖 Sorry, no matching packages found in {selected_state}. Try adjusting filters!")

    else:
        st.write("🤖 Please specify a state to get relevant packages.")


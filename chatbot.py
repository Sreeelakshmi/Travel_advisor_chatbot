import pandas as pd
import google.generativeai as genai
import streamlit as st

# Load travel package data
data_path = 'Seven_Sisters_Travel_Packages.csv'
df = pd.read_csv(data_path)

# Configure Gemini API
genai.configure(api_key="AIzaSyDNwIxW9HofySRWVYeAjkXTA5by_5LF-j0")

def fetch_package_info(state, family_friendly=None, budget=None):
    """Fetches travel package details for a given state with optional filters."""
    packages = df[df['State'].str.lower() == state.lower()]

    # Check if "Family_Friendly" column exists before filtering
    if 'Family_Friendly' in df.columns and family_friendly is not None:
        packages = packages[packages['Family_Friendly'].str.lower() == "yes"] if family_friendly else packages

    # Check if "Budget(INR)" column exists before filtering
    if budget is not None and 'Budget(INR)' in df.columns:
        packages = packages[pd.to_numeric(packages['Budget(INR)'], errors='coerce') <= budget]

    if packages.empty:
        return "No travel packages available for this selection."
    
    return packages.to_string(index=False)

def fetch_general_info(state):
    """Uses Gemini API to fetch general information about a state with a diverse keyword search."""
    keywords = ["tourism", "culture", "history", "best places to visit", "food", "festivals", "geography", "climate", "local traditions", "wildlife", "heritage sites", "transportation options", "adventure activities", "shopping", "accommodation"]
    keyword_prompt = ', '.join(keywords)
    prompt = f"Provide a comprehensive travel guide about {state}, one of the Seven Sisters of India. Cover aspects such as {keyword_prompt}."
    response = genai.generate_text(prompt)
    return response.text if response else "No information found."

def chatbot_response(user_input):
    """Processes user input to determine the response."""
    words = user_input.lower().split()
    for state in df['State'].unique():
        if state.lower() in words:
            package_info = fetch_package_info(state)
            general_info = fetch_general_info(state)
            return f"{general_info}\n\n### 📦 Travel Packages:\n{package_info}"
    return "Please specify a state from the Seven Sisters of India."

# Streamlit UI
st.set_page_config(page_title="Seven Sisters Travel Chatbot", page_icon="🌍", layout="wide")
st.title("🌏 Seven Sisters Travel Chatbot")
st.markdown("Welcome to the **Seven Sisters Travel Chatbot**! Ask me about any of the Seven Sisters states, and I'll provide travel insights along with package details.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me about any state from the Seven Sisters!")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    response = chatbot_response(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Sidebar for additional information
st.sidebar.title("🗺️ About the Seven Sisters")
st.sidebar.info("The Seven Sisters of India are Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, and Tripura. Each state has its own unique culture, traditions, and breathtaking landscapes.")

st.sidebar.title("📌 How to Use")
st.sidebar.write("1. Type your question in the chat input below.\n2. Get detailed travel insights and available packages.\n3. Explore the sidebar for more details about the region.")

# Ensure correct column name
budget_col = 'Budget(INR)'

# Sidebar for Travel Packages
st.sidebar.title("🏝️ Travel Packages")
st.sidebar.write("Select a state to see available travel packages.")
selected_state = st.sidebar.selectbox("Choose a State", df['State'].unique())

# Filters for travel packages
family_friendly = st.sidebar.checkbox("Family Friendly")

# Ensure the column exists and is numeric
if budget_col in df.columns:
    df[budget_col] = pd.to_numeric(df[budget_col], errors='coerce')
    df.dropna(subset=[budget_col], inplace=True)
    min_budget = int(df[budget_col].min())
    max_budget = int(df[budget_col].max())
else:
    min_budget, max_budget = 5000, 50000  # Default values

budget = st.sidebar.slider("Budget (INR)", min_value=min_budget, max_value=max_budget, value=max_budget)

if selected_state:
    sidebar_package_info = fetch_package_info(selected_state, family_friendly=family_friendly, budget=budget)
    st.sidebar.text_area("Available Packages", sidebar_package_info, height=200)

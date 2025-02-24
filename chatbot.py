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

    if 'Family_Friendly' in df.columns and family_friendly is not None:
        packages = packages[packages['Family_Friendly'].str.lower() == "yes"] if family_friendly else packages

    if budget is not None and 'Budget(INR)' in df.columns:
        packages = packages[pd.to_numeric(packages['Budget(INR)'], errors='coerce') <= budget]

    return packages.to_string(index=False) if not packages.empty else "No travel packages available for this selection."

def fetch_general_info(state):
    """Fetches general travel information using Gemini API."""
    keywords = ["tourism", "culture", "history", "best places to visit", "food", "festivals", "geography", "climate", "local traditions", "wildlife", "heritage sites", "transportation options", "adventure activities", "shopping", "accommodation"]
    keyword_prompt = ', '.join(keywords)
    prompt = f"Provide a detailed travel guide about {state}, covering aspects such as {keyword_prompt}."
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.candidates[0].text if response and response.candidates else "No information found."
    except Exception as e:
        return "Sorry, I couldn't retrieve information at the moment. Please try again later."

def chatbot_response(user_input):
    """Processes user input to determine the response."""
    words = user_input.lower().split()
    for state in df['State'].unique():
        if state.lower() in words:
            package_info = fetch_package_info(state)
            general_info = fetch_general_info(state)
            return f"### 🌍 Travel Guide for {state}\n\n{general_info}\n\n### 📦 Available Travel Packages:\n{package_info}"
    return "Please specify a state from the Seven Sisters of India."

# Streamlit UI
st.set_page_config(page_title="Seven Sisters Travel Chatbot", page_icon="🌍", layout="wide")
st.title("🌏 Seven Sisters Travel Chatbot")
st.markdown("Welcome! Ask me about any of the Seven Sisters states, and I'll provide travel insights along with package details.")

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

# Sidebar Information
st.sidebar.title("🗺️ About the Seven Sisters")
st.sidebar.info("The Seven Sisters of India are Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, and Tripura. Each state has unique culture, traditions, and breathtaking landscapes.")

st.sidebar.title("📌 How to Use")
st.sidebar.write("1. Type your question in the chat input.\n2. Get detailed travel insights and available packages.\n3. Explore the sidebar for more details about the region.")

# Sidebar Travel Packages
st.sidebar.title("🏝️ Travel Packages")
st.sidebar.write("Select a state to see available travel packages.")
selected_state = st.sidebar.selectbox("Choose a State", df['State'].unique())

family_friendly = st.sidebar.checkbox("Family Friendly")

budget_col = 'Budget(INR)'
if budget_col in df.columns:
    df[budget_col] = pd.to_numeric(df[budget_col], errors='coerce')
    df.dropna(subset=[budget_col], inplace=True)
    min_budget, max_budget = int(df[budget_col].min()), int(df[budget_col].max())
else:
    min_budget, max_budget = 5000, 50000  # Default values

budget = st.sidebar.slider("Budget (INR)", min_value=min_budget, max_value=max_budget, value=max_budget)

if selected_state:
    sidebar_package_info = fetch_package_info(selected_state, family_friendly=family_friendly, budget=budget)
    st.sidebar.text_area("Available Packages", sidebar_package_info, height=200)

import pandas as pd
import google.generativeai as genai
import streamlit as st

# Load travel package data
data_path = '/mnt/data/Seven_Sisters_Travel_Packages.csv'
df = pd.read_csv(data_path)

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def fetch_package_info(state):
    """Fetches travel package details for a given state."""
    packages = df[df['State'].str.lower() == state.lower()]
    if packages.empty:
        return "No travel packages available for this state."
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

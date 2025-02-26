import pandas as pd
import streamlit as st

# Dictionary containing general travel information
seven_sisters_info = {
    "Arunachal Pradesh": { ... },  # Keep the detailed dictionary here
    "Assam": { ... },
    "Manipur": { ... },
    "Meghalaya": { ... },
    "Mizoram": { ... },
    "Nagaland": { ... },
    "Tripura": { ... }
}

# Load travel package data
data_path = 'Seven_Sisters_Travel_Packages.csv'
df = pd.read_csv(data_path)

def fetch_package_info(state, family_friendly=None, budget=None):
    packages = df[df['State'].str.lower() == state.lower()]
    if 'Family_Friendly' in df.columns and family_friendly is not None:
        packages = packages[packages['Family_Friendly'].str.lower() == "yes"] if family_friendly else packages
    if budget is not None and 'Budget(INR)' in df.columns:
        packages = packages[pd.to_numeric(packages['Budget(INR)'], errors='coerce') <= budget]
    return packages.to_string(index=False) if not packages.empty else "No travel packages available."

def fetch_general_info(state):
    return seven_sisters_info.get(state, "No information available.")

def chatbot_response(user_input):
    words = user_input.lower().split()
    for state in seven_sisters_info.keys():
        if state.lower() in words:
            general_info = fetch_general_info(state)
            package_info = fetch_package_info(state)
            return f"""### 🏞️ General Information:
{general_info}\n\n### 📦 Travel Packages:
{package_info}"""
    return "Please specify a state from the Seven Sisters of India."

# Streamlit UI
st.set_page_config(page_title="Seven Sisters Travel Chatbot", page_icon="🌍", layout="wide")
st.title("🌏 Seven Sisters Travel Chatbot")
st.markdown("Welcome! Ask me about any Seven Sisters state for travel insights and package details.")

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

# Sidebar
st.sidebar.title("🗺️ About the Seven Sisters")
st.sidebar.info("These states are Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, and Tripura.")
st.sidebar.title("📌 How to Use")
st.sidebar.write("1. Type your question in the chat.")

st.sidebar.title("🏝️ Travel Packages")
selected_state = st.sidebar.selectbox("Choose a State", df['State'].unique())
family_friendly = st.sidebar.checkbox("Family Friendly")
budget = st.sidebar.slider("Budget (INR)", min_value=5000, max_value=50000, value=50000)

if selected_state:
    sidebar_package_info = fetch_package_info(selected_state, family_friendly, budget)
    st.sidebar.text_area("Available Packages", sidebar_package_info, height=200)

import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("Seven_Sisters_Travel_Packages.csv")

# Dictionary containing travel information
seven_sisters_info = {
    "Arunachal Pradesh": {
        "History": "Arunachal Pradesh has a long history of tribal heritage, influenced by Tibetan Buddhism and indigenous traditions. It was part of Assam during British rule and later became a state in 1987.",
        "Best Places": "Tawang, Ziro Valley, Namdapha National Park, Dirang",
        "Best Time": "October to April",
        "Food": "Thukpa, Momos, Bamboo Shoot Dishes, Pika Pila",
        "Culture": "Tribal culture with over 26 major tribes, vibrant festivals like Losar and Nyokum",
        "Travel Options": "Flights to Itanagar, road travel from Assam"
    },
    "Assam": {
        "History": "Assam has a rich history, with the Ahom dynasty ruling for over 600 years. It has seen influences from the Mauryan empire to British colonization, shaping its diverse culture.",
        "Best Places": "Kaziranga National Park, Majuli, Sivasagar, Kamakhya Temple",
        "Best Time": "November to April",
        "Food": "Masor Tenga, Assam Laksa, Pithas, Duck Meat Curry",
        "Culture": "Blend of Assamese, Bodo, and other indigenous cultures, Bihu festival, Satriya dance",
        "Travel Options": "Flights to Guwahati, trains, and road travel"
    }
}

st.set_page_config(page_title="Seven Sisters Travel Guide", layout="wide")
st.title("🌍 Explore Northeast India: Travel Chatbot")

# Initialize session state if not already present
if "state_selected" not in st.session_state:
    st.session_state.state_selected = None
if "info_selected" not in st.session_state:
    st.session_state.info_selected = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Greet user
query = st.text_input("Say hi to begin!", key="query_input")
send = st.button("Send")

if send and query.lower() in ["hi", "hello", "hey"]:
    st.session_state.conversation.append("🤖 Bot: Hello! Which of the Seven Sisters are you planning to visit?")
    st.session_state.state_selected = st.selectbox("Choose a state:", list(seven_sisters_info.keys()), key="state_select")

if st.session_state.state_selected:
    st.session_state.conversation.append(f"🧑‍💻 You: {st.session_state.state_selected}")
    st.session_state.conversation.append("🤖 Bot: What would you like to know about this state?")
    st.session_state.info_selected = st.selectbox("Choose a topic:", ["History", "Best Places", "Best Time", "Food", "Culture", "Travel Options", "Exit"], key="info_select")

if st.session_state.info_selected and st.session_state.info_selected != "Exit":
    info = seven_sisters_info[st.session_state.state_selected].get(st.session_state.info_selected, "Information not available.")
    st.session_state.conversation.append(f"🤖 Bot: {info}")

for message in st.session_state.conversation:
    st.write(message)


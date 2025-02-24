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
    },
    "Manipur": {
        "History": "Manipur has a deep historical significance, once ruled by the Meitei kingdom and later integrated into India in 1949.",
        "Best Places": "Loktak Lake, Kangla Fort, Keibul Lamjao National Park",
        "Best Time": "October to March",
        "Food": "Eromba, Singju, Chak-hao Kheer",
        "Culture": "Rich cultural heritage, classical Manipuri dance, Lai Haraoba festival",
        "Travel Options": "Flights to Imphal, road travel from Nagaland and Assam"
    },
    "Meghalaya": {
        "History": "Meghalaya was carved out of Assam in 1972 and is known for its matrilineal society and indigenous Khasi, Jaintia, and Garo tribes.",
        "Best Places": "Cherrapunji, Shillong, Dawki, Living Root Bridges",
        "Best Time": "October to June",
        "Food": "Jadoh, Dohneiiong, Bamboo Shoots",
        "Culture": "Khasi, Jaintia, and Garo cultures, Wangala festival, Nongkrem dance",
        "Travel Options": "Flights to Shillong, road travel from Guwahati"
    },
    "Mizoram": {
        "History": "Mizoram was initially part of Assam and became a separate state in 1987, home to the Mizo people.",
        "Best Places": "Aizawl, Phawngpui National Park, Vantawng Falls",
        "Best Time": "November to March",
        "Food": "Bai, Misa Mach Poora, Bamboo Shoot dishes",
        "Culture": "Mizo traditions, Chapchar Kut festival, rich folk music",
        "Travel Options": "Flights to Aizawl, road travel from Assam"
    },
    "Nagaland": {
        "History": "Nagaland became a state in 1963, home to various Naga tribes with a history of resilience and traditions.",
        "Best Places": "Kohima, Dzukou Valley, Hornbill Festival",
        "Best Time": "October to May",
        "Food": "Smoked Pork, Bamboo Shoots, Akhuni",
        "Culture": "Naga tribal heritage, Hornbill Festival, vibrant traditional attire",
        "Travel Options": "Flights to Dimapur, road travel from Assam"
    },
    "Tripura": {
        "History": "Tripura has a mix of Bengali and indigenous cultures, ruled by the Manikya dynasty before merging with India in 1949.",
        "Best Places": "Ujjayanta Palace, Neermahal, Jampui Hills",
        "Best Time": "September to March",
        "Food": "Mui Borok, Fish stews, Mosdeng Serma",
        "Culture": "Blend of Tripuri and Bengali cultures, Garia Puja, Kharchi festival",
        "Travel Options": "Flights to Agartala, road travel from Assam"
    }
}

st.set_page_config(page_title="Seven Sisters Travel Guide", layout="wide")
st.title("🌍 Explore Northeast India: Travel Chatbot")

# Sidebar filters
st.sidebar.header("Filter Travel Packages")
budget = st.sidebar.slider("Select Budget Range:", 1000, 50000, (5000, 20000))
transport = st.sidebar.selectbox("Preferred Mode of Transport", ["Any", "Flight", "Train", "Road"])
family_friendly = st.sidebar.checkbox("Family-Friendly Packages")

# Initialize session state
if "state_selected" not in st.session_state:
    st.session_state.state_selected = None
if "info_selected" not in st.session_state:
    st.session_state.info_selected = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Chatbot flow
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
    info = seven_sisters_info[st.session_state.state_selected].get(st.session_state.info_selected, "Detailed information is not available. Try another topic.")
    st.session_state.conversation.append(f"🤖 Bot: {info}")

for message in st.session_state.conversation:
    st.write(message)

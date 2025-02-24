import pandas as pd
import google.generativeai as genai
import streamlit as st

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

# Load travel package data
data_path = 'Seven_Sisters_Travel_Packages.csv'
df = pd.read_csv(data_path)

# Configure Gemini API
genai.configure(api_key="YOUR_API_KEY")

def fetch_package_info(state, family_friendly=None, budget=None):
    """Fetches best two travel package options based on user preferences."""
    packages = df[df['State'].str.lower() == state.lower()]

    if family_friendly is not None:
        packages = packages[packages['Family_Friendly'].str.lower() == "yes"] if family_friendly else packages

    if budget is not None:
        packages = packages[pd.to_numeric(packages['Budget(INR)'], errors='coerce') <= budget]
    
    return packages.head(2).to_string(index=False) if not packages.empty else "No suitable travel packages available."

def fetch_general_info(state):
    """Fetches general travel information from the dictionary."""
    return seven_sisters_info.get(state, "No information available for this state.")

def chatbot_response(user_input):
    """Processes user input to determine the response."""
    words = user_input.lower().split()
    for state in seven_sisters_info.keys():
        if state.lower() in words:
            return f"### 🌍 Travel Guide for {state}\n\n" + "\n".join([f"**{key}:** {value}" for key, value in seven_sisters_info[state].items()])
    return "Please specify a state from the Seven Sisters of India."

# Streamlit UI
st.set_page_config(page_title="Seven Sisters Travel Chatbot", page_icon="🌍", layout="wide")
st.title("🌏 Seven Sisters Travel Chatbot")

user_input = st.text_input("Ask me about any state from the Seven Sisters!")
if user_input:
    response = chatbot_response(user_input)
    st.markdown(response)

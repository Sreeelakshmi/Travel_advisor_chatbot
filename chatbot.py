import pandas as pd
import google.generativeai as genai
import streamlit as st

# Dictionary containing travel information
seven_sisters_info = {
    "Arunachal Pradesh": {
        "History": "historical significance of Arunachal Pradesh",
        "Best Places": "top attractions in Arunachal Pradesh",
        "Best Time": "ideal time to visit Arunachal Pradesh",
        "Food": "famous dishes of Arunachal Pradesh",
        "Culture": "festivals of Arunachal Pradesh",
        "Travel Options": "how to reach Arunachal Pradesh"
    },
    "Assam": {
        "History": "historical significance of Assam",
        "Best Places": "top attractions in Assam",
        "Best Time": "ideal time to visit Assam",
        "Food": "famous dishes of Assam",
        "Culture": "festivals of Assam",
        "Travel Options": "how to reach Assam"
    },
    "Manipur": {
        "History": "historical significance of Manipur",
        "Best Places": "top attractions in Manipur",
        "Best Time": "ideal time to visit Manipur",
        "Food": "famous dishes of Manipur",
        "Culture": "festivals of Manipur",
        "Travel Options": "how to reach Manipur"
    },
    "Meghalaya": {
        "History": "historical significance of Meghalaya",
        "Best Places": "top attractions in Meghalaya",
        "Best Time": "ideal time to visit Meghalaya",
        "Food": "famous dishes of Meghalaya",
        "Culture": "festivals of Meghalaya",
        "Travel Options": "how to reach Meghalaya"
    },
    "Mizoram": {
        "History": "historical significance of Mizoram",
        "Best Places": "top attractions in Mizoram",
        "Best Time": "ideal time to visit Mizoram",
        "Food": "famous dishes of Mizoram",
        "Culture": "festivals of Mizoram",
        "Travel Options": "how to reach Mizoram"
    },
    "Nagaland": {
        "History": "historical significance of Nagaland",
        "Best Places": "top attractions in Nagaland",
        "Best Time": "ideal time to visit Nagaland",
        "Food": "famous dishes of Nagaland",
        "Culture": "festivals of Nagaland",
        "Travel Options": "how to reach Nagaland"
    },
    "Tripura": {
        "History": "historical significance of Tripura",
        "Best Places": "top attractions in Tripura",
        "Best Time": "ideal time to visit Tripura",
        "Food": "famous dishes of Tripura",
        "Culture": "festivals of Tripura",
        "Travel Options": "how to reach Tripura"
    }
}

# Load travel package data
data_path = 'Seven_Sisters_Travel_Packages.csv'
df = pd.read_csv(data_path)

# Configure Gemini API
genai.configure(api_key="AIzaSyDNwIxW9HofySRWVYeAjkXTA5by_5LF-j0")

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
            return f"### 🌍 Travel Guide for {state}\n\n{fetch_general_info(state)}"
    return "Please specify a state from the Seven Sisters of India."

# Streamlit UI
st.set_page_config(page_title="Seven Sisters Travel Chatbot", page_icon="🌍", layout="wide")
st.title("🌏 Seven Sisters Travel Chatbot")

user_input = st.text_input("Ask me about any state from the Seven Sisters!")
if user_input:
    response = chatbot_response(user_input)
    st.markdown(response)

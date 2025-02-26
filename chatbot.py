import pandas as pd
import streamlit as st

# Dictionary containing general travel information
seven_sisters_info = {
    "Arunachal Pradesh": {
        "History": "Arunachal Pradesh was historically known as the North-East Frontier Agency and became a state in 1987.",
        "Best Places": "Tawang, Ziro Valley, Namdapha National Park",
        "Best Time": "October to April",
        "Food": "Thukpa, Apong (Rice Beer), Bamboo Shoot Curry",
        "Culture": "Home to various tribes like Monpa and Nyishi, known for Losar Festival",
        "Travel Options": "Flights to Itanagar, road travel from Assam"
    },
    "Assam": {
        "History": "Assam has a rich history with the Ahom dynasty ruling for over 600 years before British annexation.",
        "Best Places": "Kaziranga National Park, Majuli, Kamakhya Temple",
        "Best Time": "November to April",
        "Food": "Masor Tenga, Pithas, Assam Tea",
        "Culture": "Bihu Festival, Assamese silk weaving, Satriya dance",
        "Travel Options": "Flights to Guwahati, well-connected by road and rail"
    },
    "Manipur": {
        "History": "Manipur was once ruled by the Meitei kingdom and was integrated into India in 1949.",
        "Best Places": "Loktak Lake, Kangla Fort, Keibul Lamjao National Park",
        "Best Time": "October to March",
        "Food": "Eromba, Singju, Chak-hao Kheer",
        "Culture": "Rich cultural heritage, classical Manipuri dance, Lai Haraoba festival",
        "Travel Options": "Flights to Imphal, road travel from Nagaland and Assam"
    },
    "Meghalaya": {
        "History": "Meghalaya was part of Assam until it became a separate state in 1972.",
        "Best Places": "Cherrapunji, Shillong, Living Root Bridges",
        "Best Time": "September to May",
        "Food": "Jadoh, Tungrymbai, Dohneiiong",
        "Culture": "Khasi and Garo tribes, Wangala Festival",
        "Travel Options": "Flights to Shillong or road travel from Guwahati"
    },
    "Mizoram": {
        "History": "Mizoram was previously part of Assam and became a full-fledged state in 1987.",
        "Best Places": "Aizawl, Vantawng Falls, Phawngpui National Park",
        "Best Time": "October to March",
        "Food": "Bai, Bamboo Shoot Fry, Misa Mach Poora",
        "Culture": "Mizo tribe traditions, Chapchar Kut Festival",
        "Travel Options": "Flights to Aizawl, road travel from Assam"
    },
    "Nagaland": {
        "History": "Nagaland was created in 1963, primarily inhabited by various Naga tribes.",
        "Best Places": "Kohima, Dzukou Valley, Hornbill Festival Grounds",
        "Best Time": "October to May",
        "Food": "Smoked Pork, Bamboo Steamed Fish, Axone",
        "Culture": "16 Naga tribes, Hornbill Festival",
        "Travel Options": "Flights to Dimapur, road travel from Assam"
    },
    "Tripura": {
        "History": "Tripura was a princely state before joining India in 1949.",
        "Best Places": "Ujjayanta Palace, Neermahal, Jampui Hills",
        "Best Time": "October to March",
        "Food": "Mui Borok, Gudok, Kosoi Bwtwi",
        "Culture": "Influences from Bengali and tribal traditions, Kharchi Festival",
        "Travel Options": "Flights to Agartala, road and rail connectivity"
    }
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
    return packages.head(2).to_string(index=False) if not packages.empty else "No travel packages available."

def fetch_general_info(state, category=None):
    info = seven_sisters_info.get(state, {})
    return info.get(category, "No information available.") if category else info

def chatbot_response(user_input):
    words = user_input.lower().split()
    for state in seven_sisters_info.keys():
        if state.lower() in words:
            category_map = {
                "history": "History",
                "places": "Best Places",
                "time": "Best Time",
                "food": "Food",
                "culture": "Culture",
                "travel": "Travel Options"
            }
            for key, category in category_map.items():
                if key in words:
                    return f"### 📜 {category} of {state}:\n{fetch_general_info(state, category)}"
            general_info = fetch_general_info(state)
            package_info = fetch_package_info(state)
            return f"### 🏞️ General Information:\n{general_info}\n\n### 📦 Best Travel Packages:\n{package_info}"
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

import streamlit as st
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt")

df = pd.read_csv("Seven_Sisters_Travel_Packages.csv")

df["Processed"] = (
    df["State"].fillna("") + " " +
    df["Weather"].fillna("") + " " +
    df["Activities"].fillna("") + " " +
    df["Cultural Highlights"].fillna("")
)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Processed"])

def get_best_match(query, budget=None, transport=None, family_friendly=None):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    best_index = similarities.argmax()
    best_match = df.iloc[best_index]
    return best_match

seven_sisters_info = {
    "Arunachal Pradesh": {
        "Best Places": "Tawang, Ziro Valley, Namdapha National Park, Dirang",
        "Best Time": "October to April",
        "Cuisines": "Thukpa, Momos, Bamboo Shoot Dishes, Pika Pila",
        "Culture": "Tribal culture with over 26 major tribes, rich traditions, and vibrant festivals like Losar and Nyokum",
        "Nearby Attractions": "Bomdila, Sela Pass, Itanagar",
        "History": "Arunachal Pradesh has a long history of tribal heritage, influenced by Tibetan Buddhism and indigenous traditions. It was part of the Assam region during British rule and later became a union territory before achieving statehood in 1987."
    },
    "Assam": {
        "Best Places": "Kaziranga National Park, Majuli, Sivasagar, Kamakhya Temple",
        "Best Time": "November to April",
        "Cuisines": "Masor Tenga, Assam Laksa, Pithas, Duck Meat Curry",
        "Culture": "Blend of Assamese, Bodo, and other indigenous cultures, Bihu festival, Satriya dance",
        "Nearby Attractions": "Hajo, Manas National Park, Tezpur",
        "History": "Assam has a rich historical background, with the Ahom dynasty ruling for over 600 years. The region has seen various influences, from the Mauryan empire to British colonization, shaping its diverse culture and traditions."
    }
}

def get_state_info(state):
    state = state.strip().title()
    for key in seven_sisters_info.keys():
        if state in key:
            info = seven_sisters_info[key]
            return (f"🏔️ **{key} Travel Guide**\n"
                    f"- **Best Places to Visit:** {info['Best Places']}\n"
                    f"- **Best Time to Visit:** {info['Best Time']}\n"
                    f"- **Local Cuisines:** {info['Cuisines']}\n"
                    f"- **Culture:** {info['Culture']}\n"
                    f"- **Nearby Attractions:** {info['Nearby Attractions']}\n"
                    f"- **History:** {info['History']}")
    return "Sorry, I don't have detailed information on that state. Try specifying a state from the Seven Sisters."

st.set_page_config(page_title="Seven Sisters Travel Guide", layout="wide")
st.sidebar.title("🔍 Travel Search")
budget = st.sidebar.selectbox("Select Budget:", ["Any", "Low", "Medium", "High"])
transport = st.sidebar.selectbox("Preferred Transport:", ["Any", "Bus", "Train", "Flight"])
family_friendly = st.sidebar.checkbox("Family-Friendly")

st.title("🌍 Explore Northeast India: Travel Chatbot")
st.write("Hello! I'm your travel assistant. How can I help you today? Type your query below.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

query = st.text_input("Enter your query:", key="query_input")
send = st.button("Send")

if send and query:
    st.session_state.conversation.append(f"🧑‍💻 You: {query}")
    response = get_state_info(query)
    st.session_state.conversation.append(f"🤖 Bot: {response}")

for message in st.session_state.conversation:
    st.write(message)


import pandas as pd
import streamlit as st

# Dictionary containing general travel information
# Dictionary containing general travel information
seven_sisters_info = {
    "Arunachal Pradesh": {
        "History": "Arunachal Pradesh, known as the 'Land of the Rising Sun,' has a rich history influenced by the Monpa Kingdoms, Tibetan culture, and British colonial rule. It became a full-fledged state of India in 1987. The region has historical ties with Tibet and has seen conflicts like the 1962 Indo-China War. The state's history is deeply connected with indigenous tribes and their traditions, including the rule of the Chutia and Ahom dynasties in certain regions.",
        "Best Places": "Tawang Monastery, Ziro Valley, Namdapha National Park, Sela Pass, Bomdila, Itanagar, Mechuka Valley, Dirang, and Pasighat. These locations offer a mix of cultural, spiritual, and adventure experiences, attracting nature lovers and history enthusiasts alike.",
        "Best Time": "October to April is ideal, as the weather is cool and suitable for sightseeing, trekking, and festivals. The monsoon season can make travel difficult due to landslides.",
        "Food": "Apong (rice beer), Thukpa, Zan, Momos, Pika Pila, Bamboo Shoot Dishes, Chura Sabzi, and Marua. Traditional tribal cuisine is heavily influenced by fermented ingredients and locally grown vegetables.",
        "Culture": "A mix of Buddhist, Tibetan, and indigenous tribal traditions. Famous for festivals like Losar, Reh, Si-Donyi, Nyokum, and Solung. The diverse tribal communities celebrate unique rituals and dances.",
        "Travel Options": "Flights to Itanagar, road trips from Assam, and rail connectivity to Naharlagun. [Book on MakeMyTrip](https://www.makemytrip.com/) or [Yatra](https://www.yatra.com/)"
    },
    "Assam": {
        "History": "Assam has a deep-rooted history influenced by the Ahom Dynasty, the Mughals, and the British colonial era. The Battle of Saraighat (1671) was a key historical event where the Ahoms defeated the Mughals. Assam played a vital role in India's independence movement and tea cultivation. The state has a long history of trade, commerce, and cultural evolution influenced by neighboring states and foreign traders.",
        "Best Places": "Kaziranga National Park, Majuli Island, Kamakhya Temple, Sivasagar, Tezpur, Manas National Park, Haflong, Pobitora Wildlife Sanctuary, and Jorhat. Each location has its own unique blend of history, spirituality, and natural beauty.",
        "Best Time": "November to April offers comfortable weather for exploring wildlife, temples, and scenic river cruises. Summers can be hot, while monsoons bring lush greenery but also heavy rainfall.",
        "Food": "Assamese Thali, Masor Tenga, Pitha, Khar, Duck Curry, Bamboo Shoot Dishes, Paro Mangxo, and Pani Tenga. The cuisine is simple yet flavorful, featuring minimal oil and a perfect balance of spices.",
        "Culture": "Famous for Bihu dance, Sattriya dance, traditional silk weaving, and Assamese Vaishnavism. The state has a mix of tribal and non-tribal influences, and its vibrant festivals are deeply rooted in agricultural cycles.",
        "Travel Options": "Direct flights to Guwahati, train connectivity, and road trips from Meghalaya and West Bengal. [Book on MakeMyTrip](https://www.makemytrip.com/) or [Cleartrip](https://www.cleartrip.com/)"
    },
    "Manipur": {
        "History": "Manipur has a deep historical significance, once ruled by the Meitei kingdom and later integrated into India in 1949. The state played a crucial role during World War II, with major battles fought here between the British and Japanese forces. It has a rich history of kingship, with cultural and political ties extending to Myanmar and Southeast Asia.",
        "Best Places": "Loktak Lake, Kangla Fort, Keibul Lamjao National Park, Shirui Hills, Imphal, Andro Village, and Thoubal. Each of these places has a unique charm, from serene floating islands to historical sites.",
        "Best Time": "October to March is the best time to visit, with pleasant weather for sightseeing and outdoor activities. Summers can be warm, while monsoons bring heavy rainfall.",
        "Food": "Eromba, Singju, Chak-hao Kheer, Morok Metpa, Kangshoi, and Ngari-based dishes. The cuisine is known for its use of fermented ingredients and fresh vegetables.",
        "Culture": "Rich cultural heritage with Manipuri classical dance, Lai Haraoba festival, and indigenous Meitei traditions. The state's dance forms are internationally recognized for their grace and spirituality.",
        "Travel Options": "Flights to Imphal, road travel from Nagaland and Assam. [Book on MakeMyTrip](https://www.makemytrip.com/) or [Expedia](https://www.expedia.co.in/)"
    },
    "Mizoram": {
        "History": "Mizoram has a history influenced by tribal migrations, British colonization, and its transition from a Union Territory to full statehood in 1987. The region was historically inhabited by the Lushai tribes.",
        "Best Places": "Aizawl, Reiek, Phawngpui National Park, Vantawng Falls, Champhai, and Tam Dil Lake.",
        "Best Time": "October to March, when the weather is cool and suitable for exploration.",
        "Food": "Bai, Bamboo Shoot Curry, Misa Mach Poora, and Sanpiau.",
        "Culture": "Strong tribal traditions, music, and festivals like Chapchar Kut and Pawl Kut.",
        "Travel Options": "Flights to Aizawl, road travel from Assam. [Book on MakeMyTrip](https://www.makemytrip.com/)"
    },
    "Nagaland": {
        "History": "Nagaland is known for its fierce warrior tribes and rich headhunting traditions. It became a state in 1963 and is home to the famous Hornbill Festival.",
        "Best Places": "Kohima, Dzukou Valley, Mokokchung, Mon, and Tuophema Village.",
        "Best Time": "November to April, when the weather is mild and festival season peaks.",
        "Food": "Smoked Pork, Axone, Bamboo Shoot Dishes, and Galho.",
        "Culture": "Distinct tribal culture, traditional arts, and warrior traditions.",
        "Travel Options": "Flights to Dimapur, road travel from Assam. [Book on MakeMyTrip](https://www.makemytrip.com/)"
    },
    "Tripura": {
        "History": "Tripura has a long history of royal rule under the Manikya dynasty. It merged with India in 1949 and has rich cultural influences from Bengal and tribal communities.",
        "Best Places": "Ujjayanta Palace, Neermahal, Sepahijala Wildlife Sanctuary, and Unakoti.",
        "Best Time": "October to March, when the climate is cool and pleasant.",
        "Food": "Mui Borok, Gudok, Mosdeng Serma, and Muiya Awandru.",
        "Culture": "Tribal heritage, folk dances, and traditional handicrafts.",
        "Travel Options": "Flights to Agartala, road travel from Assam. [Book on MakeMyTrip](https://www.makemytrip.com/)"
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

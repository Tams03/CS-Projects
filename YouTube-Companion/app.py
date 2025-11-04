# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import get_channel_id, get_channel_data, compare_channels, compare_multiple_channels_and_recommend_with_graph, suggest_channel_based_on_others, youtube

# --- Page Config ---
st.set_page_config(page_title="YouTube Channel Analyzer", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #eaf6ea;}  /* Light green background */
    .stButton>button {background-color: #4CAF50; color: white; height: 3em; width: 100%; font-size: 16px; border-radius: 10px;}
    .stTextArea>textarea {border-radius: 10px;}
    h1 {color: #2E7D32;}
    h2 {color: #2E7D32;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 YouTube Channel Analyzer")
st.write("Analyze channels, compare them, or get new channel suggestions based on your preferences.")

# --- Sidebar Buttons ---
action = st.radio("Choose Action:", ["Compare Channels", "Get Channel Data", "Suggest Me a Channel"])

# ------------------- Compare Channels -------------------
if action == "Compare Channels":
    st.header("Compare Multiple YouTube Channels")
    channels_input = st.text_area("Enter two or more channel names (comma separated):", "")
    if st.button("Run Comparison"):
        if channels_input.strip() == "":
            st.warning("Please enter at least two channel names.")
        else:
            channel_list = [c.strip() for c in channels_input.split(",") if c.strip()]
            if len(channel_list) < 2:
                st.warning("Enter at least two channel names.")
            else:
                st.info("Fetching data...")
                compare_multiple_channels_and_recommend_with_graph(channel_list)
                st.success("Comparison complete!")

# ------------------- Get Channel Data -------------------
elif action == "Get Channel Data":
    st.header("Get Detailed Data for YouTube Channels")
    channels_input = st.text_area("Enter one or more channel names (comma separated):", "")
    if st.button("Get Data"):
        if channels_input.strip() == "":
            st.warning("Please enter at least one channel name.")
        else:
            channel_list = [c.strip() for c in channels_input.split(",") if c.strip()]
            data_list = []
            for handle in channel_list:
                cid = get_channel_id(handle)
                if not cid:
                    st.error(f"Channel '{handle}' not found.")
                    continue
                cdata = get_channel_data(cid)
                if cdata:
                    data_list.append(cdata)
            if data_list:
                df = pd.DataFrame(data_list)
                st.dataframe(df)

# ------------------- Suggest Me a Channel -------------------
elif action == "Suggest Me a Channel":
    st.header("Get a Suggested YouTube Channel")
    option = st.selectbox("Select input type:", ["Based on Channels You Like", "Based on a Topic"])
    
    if option == "Based on Channels You Like":
        channels_input = st.text_area("Enter channels you like (comma separated):", "")
        if st.button("Get Suggestion"):
            if channels_input.strip() == "":
                st.warning("Please enter at least one channel.")
            else:
                channel_list = [c.strip() for c in channels_input.split(",") if c.strip()]
                st.info("Finding a similar channel...")
                suggest_channel_based_on_others(channel_list, youtube)
    
    elif option == "Based on a Topic":
        topic_input = st.text_input("Enter a topic or keyword:", "")
        if st.button("Get Suggestion by Topic"):
            if topic_input.strip() == "":
                st.warning("Please enter a topic.")
            else:
                st.info(f"Searching for channels related to '{topic_input}'...")
                # Search YouTube by topic
                request = youtube.search().list(
                    part="snippet",
                    q=topic_input,
                    type="channel",
                    maxResults=1
                )
                response = request.execute()
                if response.get('items'):
                    channel = response['items'][0]['snippet']
                    st.success("Suggested Channel:")
                    st.markdown(f"[{channel['title']}](https://www.youtube.com/channel/{channel['channelId']})")
                else:
                    st.error("No channels found for this topic.")


# app.py
import streamlit as st
from backend.py import (
    get_channel_data,
    compare_channels,
    suggest_channel_based_on_others,
    calculate_content_frequency,
    get_most_popular_video,
    rank_channels,
    best_channel
)

st.set_page_config(page_title="YouTube Channel Analyzer", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #eaf6ea;}  /* Light green background */
        .stButton>button {background-color: #4CAF50; color: white; height: 3em; width: 100%; font-size: 16px; border-radius: 10px;}
        .stTextArea>textarea {border-radius: 10px;}
        h1, h2, h3 {color: #2E7D32;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 YouTube Channel Analyzer")
st.write("Analyze channels, compare them, or get new channel suggestions based on your preferences.")

# ------------------- Sidebar / Action -------------------
action = st.radio("Choose Action:", ["Compare Channels", "Get Channel Data", "Suggest Me a Channel"])

# ------------------- 1. Compare Channels -------------------
if action == "Compare Channels":
    st.header("Compare Multiple YouTube Channels")
    channels_input = st.text_area("Enter two or more channel names (comma or newline separated):", "")
    if st.button("Run Comparison"):
        handles = [h.strip() for h in channels_input.replace("\n", ",").split(",") if h.strip()]
        if len(handles) < 2:
            st.warning("Please enter at least two channels.")
        else:
            st.info("Fetching channel data...")
            data_list = compare_channels(handles)
            if not data_list:
                st.error("No valid channel data found.")
            else:
                # --- Comparison by Subscribers ---
                st.subheader("Channel Comparison based on Subscribers:")
                for i, ch in enumerate(rank_channels(data_list, 'Subscribers'), 1):
                    st.write(f"{i}. {ch['Handle']} - {ch['Subscribers']:,} Subscribers")

                # --- Comparison by Views ---
                st.subheader("Channel Comparison based on Views:")
                for i, ch in enumerate(rank_channels(data_list, 'Views'), 1):
                    st.write(f"{i}. {ch['Handle']} - {ch['Views']:,} Views")

                # --- Comparison by Engagement Rate ---
                st.subheader("Channel Comparison based on Engagement Rate:")
                for i, ch in enumerate(rank_channels(data_list, 'Engagement Rate (%)'), 1):
                    st.write(f"{i}. {ch['Handle']} - {ch['Engagement Rate (%)']}% Engagement Rate")

                st.markdown("---")

                # --- Recommendations ---
                best_engagement = best_channel(data_list, 'Engagement Rate (%)')
                best_views = best_channel(data_list, 'Views')
                st.subheader("Recommendations")
                st.write(f"Best Channel by Engagement Rate: {best_engagement['Handle']} ({best_engagement['Engagement Rate (%)']}%)")
                st.write(f"Best Channel by Views: {best_views['Handle']} ({best_views['Views']:,} Views)")

# ------------------- 2. Get Channel Data -------------------
elif action == "Get Channel Data":
    st.header("Get Detailed Data for YouTube Channels")
    channels_input = st.text_area("Enter one or more channel names (comma or newline separated):", "")
    if st.button("Get Data"):
        handles = [h.strip() for h in channels_input.replace("\n", ",").split(",") if h.strip()]
        if not handles:
            st.warning("Please enter at least one channel.")
        else:
            st.info("Fetching channel data...")
            for handle in handles:
                cid = None
                try:
                    from backend_v3_complete import get_channel_id
                    cid = get_channel_id(handle)
                except:
                    st.error(f"Error getting channel ID for {handle}")
                if not cid:
                    st.error(f"Channel '{handle}' not found.")
                    continue

                data = get_channel_data(cid)
                if not data:
                    st.error(f"No data for {handle}")
                    continue

                content_freq = calculate_content_frequency(cid)
                popular_video = get_most_popular_video(cid)

                st.subheader(f"Channel: {data['Handle']}")
                st.write(f"Link: {data['Link']}")
                st.write(f"Subscribers: {data['Subscribers']:,}")
                st.write(f"Views: {data['Views']:,}")
                st.write(f"Videos: {data['Videos']:,}")
                st.write(f"Content Frequency: {content_freq if content_freq else 'N/A'} days")
                st.write(f"Most Popular Video: {popular_video if popular_video else 'N/A'}")
                st.write(f"Engagement Rate: {round((data['Views']/data['Subscribers']*100) if data['Subscribers']>0 else 0, 2)}%")
                st.markdown("---")

# ------------------- 3. Suggest Me a Channel -------------------
elif action == "Suggest Me a Channel":
    st.header("Get a Suggested YouTube Channel")
    option = st.selectbox("Select input type:", ["Based on Channels You Like", "Based on a Topic"])
    
    if option == "Based on Channels You Like":
        channels_input = st.text_area("Enter channels you like (comma or newline separated):", "")
        if st.button("Get Suggestion"):
            handles = [h.strip() for h in channels_input.replace("\n", ",").split(",") if h.strip()]
            if not handles:
                st.warning("Please enter at least one channel.")
            else:
                suggestion = suggest_channel_based_on_others(handles)
                if suggestion:
                    st.success("Suggested Channel:")
                    st.markdown(f"[{suggestion['Handle']}]({suggestion['Link']})")
                else:
                    st.error("No similar channels found.")
    elif option == "Based on a Topic":
        topic = st.text_input("Enter a topic or keyword:", "")
        if st.button("Get Suggestion by Topic"):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                # Simple search suggestion
                from backend_v3_complete import youtube
                try:
                    response = youtube.search().list(part="snippet", type="channel", q=topic, maxResults=1).execute()
                    if response.get('items'):
                        ch = response['items'][0]
                        link = f"https://www.youtube.com/channel/{ch['snippet']['channelId']}"
                        st.success("Suggested Channel:")
                        st.markdown(f"[{ch['snippet']['title']}]({link})")
                    else:
                        st.error("No channels found for this topic.")
                except Exception as e:
                    st.error(f"Error searching for topic: {e}")

import streamlit as st
from backend import compare_channels, get_channel_data, suggest_channel_based_on_others
from googleapiclient.discovery import build

API_KEY = 'AIzaSyCXEhvGzLjh6IjRogjjJ3CJ2g4J9P64Yho'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# --- PAGE CONFIG ---
st.set_page_config(page_title="YouTube Companion", layout="wide")
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #eaf5ea;
    }
    /* Headers */
    h1, h2, h3 {
        color: #2e7d32;
    }
    /* Buttons */
    div.stButton > button:first-child {
        background-color: #2e7d32;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📺 YouTube Companion")
st.write("Analyze, compare, and discover YouTube channels!")

# --- SIDEBAR SELECTION ---
action = st.sidebar.radio(
    "Select Action",
    ["Get Channel Data", "Compare Channels", "Suggest New Channels"]
)

# --- ACTION 1: GET CHANNEL DATA ---
if action == "Get Channel Data":
    st.subheader("Get Channel Data")
    channel_handle = st.text_input("Enter YouTube Channel Handle:")
    
    if st.button("Get Data"):
        if channel_handle:
            data = get_channel_data(channel_handle, youtube)
            if data:
                st.success("✅ Channel Data Retrieved Successfully!")
                st.markdown(f"**Channel Name:** {data['YouTube Handle']}")
                st.markdown(f"**Subscribers:** {data.get('YouTube Subscribers', 'N/A')}")
                st.markdown(f"**Total Views:** {data.get('YouTube Views', 'N/A')}")
                st.markdown(f"**Total Videos:** {data.get('YouTube Videos', 'N/A')}")
                st.markdown(f"[Visit Channel]({data.get('YouTube Channel Link', '#')})")
            else:
                st.error("❌ Could not retrieve channel data. Check the handle.")
        else:
            st.warning("⚠️ Please enter a channel handle.")

# --- ACTION 2: COMPARE CHANNELS ---
elif action == "Compare Channels":
    st.subheader("Compare Multiple Channels")
    channel_handles_input = st.text_area(
        "Enter YouTube Channel Handles (separated by commas):"
    )
    if st.button("Compare"):
        if channel_handles_input:
            channel_handles = [h.strip() for h in channel_handles_input.split(",") if h.strip()]
            comparison = compare_channels(channel_handles, youtube)
            if comparison:
                st.success("✅ Comparison Completed!")
                for i, ch in enumerate(comparison, 1):
                    st.markdown(f"### {i}. {ch['YouTube Handle']}")
                    st.markdown(f"**Subscribers:** {ch.get('YouTube Subscribers', 'N/A')}")
                    st.markdown(f"**Views:** {ch.get('YouTube Views', 'N/A')}")
                    st.markdown(f"**Videos:** {ch.get('YouTube Videos', 'N/A')}")
                    st.markdown(f"**Most Common Category:** {ch.get('Most Common Category', 'N/A')}")
                    st.markdown(f"**Engagement Rate:** {ch.get('Engagement Rate (%)', 'N/A')}%")
                    st.markdown(f"**Content Frequency:** {ch.get('Content Frequency', 'N/A')}")
                    st.markdown(f"**Most Popular Video:** {ch.get('Most Popular Video', 'N/A')}")
                    st.markdown("---")
            else:
                st.error("❌ No valid data found for the given channels.")
        else:
            st.warning("⚠️ Please enter at least two channel handles.")

# --- ACTION 3: SUGGEST NEW CHANNELS ---
elif action == "Suggest New Channels":
    st.subheader("Suggest New Channels Based on Your Input")
    channel_handles_input = st.text_area(
        "Enter YouTube Channel Handles to Base Suggestions On (separated by commas):"
    )
    if st.button("Suggest"):
        if channel_handles_input:
            channel_handles = [h.strip() for h in channel_handles_input.split(",") if h.strip()]
            suggestion = suggest_channel_based_on_others(channel_handles, youtube)
            if suggestion:
                st.success("✅ Suggested Channel Found!")
                st.markdown(f"**Channel Name:** {suggestion.get('Channel Name', 'N/A')}")
                st.markdown(f"[Visit Channel]({suggestion.get('Channel Link', '#')})")

            else:
                st.info("ℹ️ No new similar channels could be found.")
        else:
            st.warning("⚠️ Please enter at least one channel handle.")

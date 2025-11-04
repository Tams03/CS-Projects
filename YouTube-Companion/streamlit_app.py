import streamlit as st
from backend import compare_channels, get_channel_data, suggest_channel_based_on_others, get_channel_id
from googleapiclient.discovery import build

API_KEY = 'AIzaSyCXEhvGzLjh6IjRogjjJ3CJ2g4J9P64Yho'
youtube = build('youtube', 'v3', developerKey=API_KEY)

st.set_page_config(page_title="YouTube Companion", layout="wide")
st.markdown("""
<style>
.stApp { background: linear-gradient(to bottom right, #e0f7e9, #a8e6a3, #4caf50); }
h1,h2,h3 { color:#1b5e20; }
div.stButton>button:first-child { background-color:#2e7d32; color:white; font-weight:bold; }
.stMarkdown p { color:#000000; }
</style>
""", unsafe_allow_html=True)

st.title("📺 YouTube Companion")
st.write("Analyze, compare, and discover YouTube channels!")

action = st.sidebar.radio(
    "Select Action",
    ["Get Channel Data", "Compare Channels", "Suggest New Channels"]
)

# --- Get Channel Data ---
if action == "Get Channel Data":
    st.subheader("Get Channel Data")
    channel_handle = st.text_input("Enter YouTube Channel Handle:")

    if st.button("Get Data") and channel_handle:
        channel_id = get_channel_id(channel_handle, youtube)
        if channel_id:
            data = get_channel_data(channel_id, youtube)
            if data:
                st.success("✅ Channel Data Retrieved Successfully!")
                st.markdown(f"**Handle:** {data['YouTube Handle']}")
                st.markdown(f"**Channel Link:** {data['YouTube Channel Link']}")
                st.markdown(f"**Subscribers:** {data.get('YouTube Subscribers',0):,}")
                st.markdown(f"**Views:** {data.get('YouTube Views',0):,}")
                st.markdown(f"**Videos:** {data.get('YouTube Videos',0):,}")
                st.markdown(f"**Engagement Rate:** {data.get('Engagement Rate (%)',0)}%")
                st.markdown(f"**Overall Content Category:** {data.get('Most Common Category','N/A')}")
                st.markdown(f"**Content Frequency:** {data.get('Content Frequency','N/A')}")
                st.markdown(f"**Most Popular Video:** {data.get('Most Popular Video','N/A')}")
            else:
                st.error("❌ Could not retrieve channel data. Check the handle.")
        else:
            st.error("❌ Could not find channel ID. Check the handle.")

# --- Compare Channels ---
elif action == "Compare Channels":
    st.subheader("Compare Multiple Channels")
    channel_handles_input = st.text_area("Enter YouTube Channel Handles (separated by commas):")
    if st.button("Compare") and channel_handles_input:
        channel_handles = [h.strip() for h in channel_handles_input.split(",") if h.strip()]
        comparison = compare_channels(channel_handles, youtube)
        if comparison:
            st.success("✅ Comparison Completed!")

            # Sorted outputs
            by_subs = sorted(comparison, key=lambda x: x['YouTube Subscribers'], reverse=True)
            by_views = sorted(comparison, key=lambda x: x['YouTube Views'], reverse=True)
            by_engagement = sorted(comparison, key=lambda x: x['Engagement Rate (%)'], reverse=True)

            st.markdown("### Channel Comparison based on Subscribers:")
            for i, ch in enumerate(by_subs,1):
                st.markdown(f"{i}. {ch['YouTube Handle']} - {ch['YouTube Subscribers']:,} Subscribers")

            st.markdown("### Channel Comparison based on Views:")
            for i, ch in enumerate(by_views,1):
                st.markdown(f"{i}. {ch['YouTube Handle']} - {ch['YouTube Views']:,} Views")

            st.markdown("### Channel Comparison based on Engagement Rate:")
            for i, ch in enumerate(by_engagement,1):
                st.markdown(f"{i}. {ch['YouTube Handle']} - {ch['Engagement Rate (%)']}% Engagement Rate")

            best_eng = by_engagement[0]
            best_views = by_views[0]
            st.markdown("---")
            st.markdown("**Recommendation**:")
            st.markdown(f"Best Channel by Engagement Rate: {best_eng['YouTube Handle']} with an engagement rate of {best_eng['Engagement Rate (%)']}%")
            st.markdown(f"Best Channel by Views: {best_views['YouTube Handle']} with {best_views['YouTube Views']:,} views")

        else:
            st.error("❌ No valid data found for the given channels.")

# --- Suggest New Channels ---
elif action == "Suggest New Channels":
    st.subheader("Suggest New Channels Based on Your Input")
    channel_handles_input = st.text_area("Enter YouTube Channel Handles to Base Suggestions On (separated by commas):")
    if st.button("Suggest") and channel_handles_input:
        channel_handles = [h.strip() for h in channel_handles_input.split(",") if h.strip()]
        suggestion = suggest_channel_based_on_others(channel_handles, youtube)
        if suggestion:
            st.success("✅ Suggested Channel Found!")
            st.markdown(f"**Channel Name:** {suggestion.get('Channel Name','N/A')}")
            st.markdown(f"[Visit Channel]({suggestion.get('Channel Link','#')})")
        else:
            st.info("ℹ️ No new similar channels could be found.")

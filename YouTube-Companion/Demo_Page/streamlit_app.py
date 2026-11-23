import os

import streamlit as st
from backend import compare_channels, get_channel_data, suggest_channel_based_on_others, get_channel_id
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import HttpLib2Error
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(page_title="YouTube Companion", layout="wide")

api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
if not api_key:
    try:
        api_key = st.secrets.get("YOUTUBE_API_KEY", "").strip()
    except (FileNotFoundError, StreamlitSecretNotFoundError):
        api_key = ""

if not api_key:
    st.error("Set YOUTUBE_API_KEY before running YouTube Companion.")
    st.stop()

youtube = build("youtube", "v3", developerKey=api_key)
st.title("YouTube Companion")
st.write("Look up, compare, and discover YouTube channels.")

action = st.sidebar.radio(
    "Select action", ["Get Channel Data", "Compare Channels", "Suggest New Channels"]
)
options = "Enter a channel name, @handle, ID, or channel URL"
if action == "Get Channel Data":
    raw = st.text_input(options)
    entries = [raw.strip()] if raw.strip() else []
else:
    raw = st.text_area(options + " (comma-separated)")
    entries = list(dict.fromkeys(item.strip() for item in raw.split(",") if item.strip()))

if st.button("Run"):
    if not entries or len(entries) > 5:
        st.warning("Enter between one and five channels.")
        st.stop()
    try:
        if action == "Get Channel Data":
            channel_id = get_channel_id(entries[0], youtube)
            result = get_channel_data(channel_id, youtube) if channel_id else None
            if not result:
                st.info("No unique channel found. Try its @handle or channel URL.")
            else:
                for label, value in result.items():
                    if label == "Most Popular Video":
                        label = "Most viewed sampled video"
                    st.text(f"{label}: {value if value is not None else 'Unavailable'}")
        elif action == "Compare Channels":
            results = compare_channels(entries, youtube)
            if results:
                st.dataframe(results)
                if len(results) < len(entries):
                    st.info("Some inputs referred to the same channel or could not be resolved.")
            else:
                st.info("No channels found. Try exact @handles or URLs.")
        else:
            suggestion = suggest_channel_based_on_others(entries, youtube)
            if suggestion:
                st.text(suggestion["Channel Name"])
                st.link_button("Visit channel", suggestion["Channel Link"])
            else:
                st.info("No related channel was found.")
    except HttpError as error:
        if error.resp.status in (403, 429):
            st.error("YouTube denied the request or the API quota was reached. Check your API configuration or try again later.")
        else:
            st.error("YouTube could not complete the request. Try again later.")
    except (OSError, HttpLib2Error):
        st.error("Could not connect to YouTube. Try again later.")

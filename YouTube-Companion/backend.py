# backend.py
# ---------------------------
# YouTube Channel Analyzer Backend (Streamlit Compatible)
# ---------------------------

from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------------------
# Configuration
# ---------------------------
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your YouTube API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

# ---------------------------
# Helper Functions
# ---------------------------

def get_channel_id(handle):
    """Return the channel ID for a given handle."""
    try:
        request = youtube.search().list(part='snippet', q=handle, type='channel', maxResults=1)
        response = request.execute()
        if response.get('items'):
            return response['items'][0]['id']['channelId']
    except Exception as e:
        print(f"Error in get_channel_id: {e}")
    return None

def get_channel_data(channel_id):
    """Return channel data as a dictionary."""
    try:
        request = youtube.channels().list(part='snippet,statistics', id=channel_id)
        response = request.execute()
        if response.get('items'):
            ch = response['items'][0]
            return {
                'Handle': ch['snippet']['title'],
                'Channel Link': f"https://www.youtube.com/channel/{channel_id}",
                'Subscribers': int(ch['statistics'].get('subscriberCount', 0)),
                'Views': int(ch['statistics'].get('viewCount', 0)),
                'Videos': int(ch['statistics'].get('videoCount', 0))
            }
    except Exception as e:
        print(f"Error in get_channel_data: {e}")
    return None

def calculate_content_frequency(channel_id):
    """Return average days between uploads."""
    try:
        request = youtube.activities().list(part='snippet', channelId=channel_id, maxResults=50)
        response = request.execute()
        dates = [datetime.strptime(i['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
                 for i in response.get('items', []) if 'publishedAt' in i['snippet']]
        if len(dates) > 1:
            dates.sort(reverse=True)
            intervals = [(dates[i]-dates[i+1]).days for i in range(len(dates)-1)]
            return round(sum(intervals)/len(intervals), 2)
    except Exception as e:
        print(f"Error in calculate_content_frequency: {e}")
    return None

def get_most_popular_video(channel_id):
    """Return title and link of most popular video."""
    try:
        request = youtube.search().list(part='snippet', channelId=channel_id, type='video', order='viewCount', maxResults=1)
        response = request.execute()
        if response.get('items'):
            vid = response['items'][0]
            return f"{vid['snippet']['title']} (https://www.youtube.com/watch?v={vid['id']['videoId']})"
    except Exception as e:
        print(f"Error in get_most_popular_video: {e}")
    return None

# ---------------------------
# Compare Channels
# ---------------------------

def compare_channels_data(channel_handles):
    """Return a list of dicts with detailed channel data for comparison."""
    comparison = []
    for handle in channel_handles:
        cid = get_channel_id(handle)
        if not cid:
            continue
        data = get_channel_data(cid)
        if not data:
            continue
        freq = calculate_content_frequency(cid)
        data['Content Frequency (days)'] = freq or "N/A"
        data['Most Popular Video'] = get_most_popular_video(cid) or "N/A"
        # Engagement Rate = Views / Subscribers * 100
        data['Engagement Rate (%)'] = round((data['Views']/data['Subscribers']*100) if data['Subscribers']>0 else 0, 2)
        comparison.append(data)
    return comparison

# ---------------------------
# Suggest Channels
# ---------------------------

def suggest_channel_based_on_others(channel_handles):
    """Return one suggested channel based on channels you like."""
    input_ids = [get_channel_id(h) for h in channel_handles if get_channel_id(h)]
    suggested = None
    for cid in input_ids:
        data = get_channel_data(cid)
        if data:
            search = youtube.search().list(part='snippet', type='channel', q=data['Handle'], maxResults=10).execute()
            for ch in search.get('items', []):
                if ch['snippet']['channelId'] not in input_ids:
                    suggested = {
                        'Handle': ch['snippet']['title'],
                        'Link': f"https://www.youtube.com/channel/{ch['snippet']['channelId']}"
                    }
                    break
        if suggested:
            break
    return suggested  # Returns dict or None

def suggest_channel_based_on_topic(topic):
    """Return one suggested channel based on a topic."""
    try:
        search = youtube.search().list(part='snippet', type='channel', q=topic, maxResults=1).execute()
        if search.get('items'):
            ch = search['items'][0]
            return {'Handle': ch['snippet']['title'], 'Link': f"https://www.youtube.com/channel/{ch['snippet']['channelId']}"}
    except Exception as e:
        print(f"Error in suggest_channel_based_on_topic: {e}")
    return None

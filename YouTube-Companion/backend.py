# backend.py
# ---------------------------
# YouTube Channel Analyzer Backend
# ---------------------------

# Imports
from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------------------
# Configuration
# ---------------------------
API_KEY = 'YOUR_API_KEY_HERE'  # replace with your actual API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

# ---------------------------
# Part 1 - Retrieve channel information
# ---------------------------

def get_channel_id(handle):
    """Find the channel ID by channel handle using YouTube Search API."""
    try:
        request = youtube.search().list(part='snippet', q=handle, type='channel')
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['id']['channelId']
        else:
            print(f"No channel found for handle {handle}")
            return None
    except Exception as e:
        print(f"Error finding channel ID for handle {handle}: {e}")
        return None

def get_all_video_categories(channel_id, max_results=50):
    """Fetch video categories from a channel."""
    categories = []
    try:
        request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=max_results, type='video')
        response = request.execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            video_request = youtube.videos().list(part='snippet', id=video_id)
            video_response = video_request.execute()
            if 'items' in video_response and len(video_response['items']) > 0:
                categories.append(video_response['items'][0]['snippet']['categoryId'])
    except Exception as e:
        print(f"Error fetching video categories for channel ID {channel_id}: {e}")
    return categories

def get_category_name(category_id):
    """Fetch the category name from the category ID."""
    try:
        request = youtube.videoCategories().list(part='snippet', id=category_id)
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        else:
            return None
    except Exception as e:
        print(f"Error fetching category name for category ID {category_id}: {e}")
        return None

def get_channel_data(channel_id):
    """Fetch channel data from YouTube API."""
    try:
        request = youtube.channels().list(part='snippet,statistics,contentDetails', id=channel_id)
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            info = response['items'][0]
            return {
                'YouTube Handle': info['snippet']['title'],
                'YouTube Channel Link': f"https://www.youtube.com/channel/{channel_id}",
                'YouTube Subscribers': int(info['statistics'].get('subscriberCount', 0)),
                'YouTube Views': int(info['statistics'].get('viewCount', 0)),
                'YouTube Videos': int(info['statistics'].get('videoCount', 0))
            }
        else:
            print(f"No data found for channel ID {channel_id}")
            return None
    except Exception as e:
        print(f"Error fetching data for channel ID {channel_id}: {e}")
        return None

def calculate_content_frequency(channel_id):
    """Calculate content upload frequency."""
    try:
        request = youtube.activities().list(part='snippet,contentDetails', channelId=channel_id, maxResults=50)
        response = request.execute()
        upload_dates = [
            datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
            for item in response.get('items', [])
            if 'publishedAt' in item['snippet']
        ]
        if len(upload_dates) > 1:
            upload_dates.sort(reverse=True)
            intervals = [(upload_dates[i] - upload_dates[i+1]).days for i in range(len(upload_dates)-1)]
            return sum(intervals) / len(intervals)
        else:
            return None
    except Exception as e:
        print(f"Error calculating content frequency for channel ID {channel_id}: {e}")
        return None

def get_most_popular_video(channel_id):
    """Get the most popular video for a channel."""
    try:
        request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=1, type='video', order='viewCount')
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            vid_id = video['id']['videoId']
            title = video['snippet']['title']
            return f"{title} (https://www.youtube.com/watch?v={vid_id})"
        else:
            return None
    except Exception as e:
        print(f"Error fetching most popular video for channel ID {channel_id}: {e}")
        return None

# ---------------------------
# Part 2 - Compare channels and visualize
# ---------------------------

def compare_channels(channel_handles):
    comparison_data = []
    for handle in channel_handles:
        channel_id = get_channel_id(handle)
        if not channel_id:
            continue
        categories = get_all_video_categories(channel_id)
        if categories:
            most_common_id, _ = Counter(categories).most_common(1)[0]
            category_name = get_category_name(most_common_id)
        else:
            category_name = "Unknown"
        data = get_channel_data(channel_id)
        if data:
            views = data['YouTube Views']
            subs = data['YouTube Subscribers']
            engagement = (views / subs) * 100 if subs > 0 else 0
            freq = calculate_content_frequency(channel_id)
            data['Most Common Category'] = category_name
            data['Engagement Rate (%)'] = round(engagement, 2)
            data['Content Frequency'] = f"New content every {round(freq, 2)} days" if freq else "Not enough data"
            data['Most Popular Video'] = get_most_popular_video(channel_id) or "No popular video found"
            comparison_data.append(data)
    return comparison_data

def format_number(n):
    """Format numbers with commas."""
    return f"{n:,}"

def compare_multiple_channels_and_recommend_with_graph(channel_handles):
    """Prepare data for display and recommendations."""
    data_list = compare_channels(channel_handles)
    if not data_list:
        return [], "No valid channel data found."

    # Sort channels
    sorted_by_subs = sorted(data_list, key=lambda x: x['YouTube Subscribers'], reverse=True)
    sorted_by_views = sorted(data_list, key=lambda x: x['YouTube Views'], reverse=True)
    sorted_by_engagement = sorted(data_list, key=lambda x: x['Engagement Rate (%)'], reverse=True)

    recommendation = {
        "Best by Engagement": sorted_by_engagement[0]['YouTube Handle'],
        "Engagement Rate": sorted_by_engagement[0]['Engagement Rate (%)'],
        "Best by Views": sorted_by_views[0]['YouTube Handle'],
        "Views": sorted_by_views[0]['YouTube Views']
    }

    return data_list, recommendation

# ---------------------------
# Part 3 - Suggest channels
# ---------------------------

def suggest_channel_based_on_others(channel_handles):
    """Suggest a new channel based on liked channels."""
    suggested = None
    input_ids = [get_channel_id(h) for h in channel_handles if get_channel_id(h)]
    for cid in input_ids:
        data = get_channel_data(cid)
        if data:
            search_request = youtube.search().list(part="snippet", type="channel", q=data['YouTube Handle'], maxResults=10)
            response = search_request.execute()
            for item in response['items']:
                new_cid = item['snippet']['channelId']
                if new_cid not in input_ids:
                    suggested = {
                        "title": item['snippet']['title'],
                        "link": f"https://www.youtube.com/channel/{new_cid}"
                    }
                    break
        if suggested:
            break
    return suggested

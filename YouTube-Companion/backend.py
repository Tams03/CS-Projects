# backend.py
# ---------------------------
# YouTube Channel Analyzer Backend
# ---------------------------

# Imports
from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import locale

# ---------------------------
# Configuration
# ---------------------------
API_KEY = 'AIzaSyCXEhvGzLjh6IjRogjjJ3CJ2g4J9P64Yho'
youtube = build('youtube', 'v3', developerKey=API_KEY)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# ---------------------------
# Part 1 - Retrieve channel information
# ---------------------------

def get_channel_id(handle):
    """Find the channel ID by channel handle using YouTube Search API."""
    try:
        request = youtube.search().list(part='snippet', q=handle, type='channel')
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            channel_info = response['items'][0]
            return channel_info['id']['channelId']
        else:
            print(f"No channel found for handle {handle}")
            return None
    except Exception as e:
        print(f"Error finding channel ID for handle {handle}: {e}")
        return None

def get_all_video_categories(channel_id, max_results=50):
    """Fetch a limited number of videos from the channel and return a list of categories."""
    categories = []
    try:
        request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=max_results, type='video')
        response = request.execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            video_request = youtube.videos().list(part='snippet', id=video_id)
            video_response = video_request.execute()
            if 'items' in video_response and len(video_response['items']) > 0:
                category_id = video_response['items'][0]['snippet']['categoryId']
                categories.append(category_id)
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
            channel_info = response['items'][0]
            data = {
                'YouTube Handle': channel_info['snippet']['title'],
                'YouTube Channel Link': f"https://www.youtube.com/channel/{channel_id}",
                'YouTube Subscribers': channel_info['statistics'].get('subscriberCount', '0'),
                'YouTube Views': channel_info['statistics'].get('viewCount', '0'),
                'YouTube Videos': channel_info['statistics'].get('videoCount', '0')
            }
            return data
        else:
            print(f"No data found for channel ID {channel_id}")
            return None
    except Exception as e:
        print(f"Error fetching data for channel ID {channel_id}: {e}")
        return None

def calculate_content_frequency(channel_id):
    """Calculate content upload frequency based on the last several video upload dates."""
    try:
        request = youtube.activities().list(part='snippet,contentDetails', channelId=channel_id, maxResults=50)
        response = request.execute()
        upload_dates = []
        for item in response.get('items', []):
            if 'publishedAt' in item['snippet']:
                upload_date = datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
                upload_dates.append(upload_date)
        if len(upload_dates) > 1:
            upload_dates.sort(reverse=True)
            intervals = [(upload_dates[i] - upload_dates[i+1]).days for i in range(len(upload_dates)-1)]
            avg_interval = sum(intervals) / len(intervals)
            return avg_interval
        else:
            return None
    except Exception as e:
        print(f"Error calculating content frequency for channel ID {channel_id}: {e}")
        return None

def get_most_popular_video(channel_id):
    """Get the most popular video (highest view count) for a given channel."""
    try:
        request = youtube.search().list(part='snippet', channelId=channel_id, maxResults=1, type='video', order='viewCount')
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            popular_video = response['items'][0]
            video_id = popular_video['id']['videoId']
            video_title = popular_video['snippet']['title']
            return f"{video_title} (https://www.youtube.com/watch?v={video_id})"
        else:
            return None
    except Exception as e:
        print(f"Error fetching most popular video for channel ID {channel_id}: {e}")
        return None

def compare_channels(channel_handles):
    """Compare channels by retrieving their predominant categories and engagement rates."""
    comparison_data = []
    for handle in channel_handles:
        channel_id = get_channel_id(handle)
        if not channel_id:
            continue
        categories = get_all_video_categories(channel_id)
        if not categories:
            print(f"Unable to retrieve categories for channel {handle}.")
            continue
        if categories:
            most_common_category_id, _ = Counter(categories).most_common(1)[0]
            category_name = get_category_name(most_common_category_id)
            channel_data = get_channel_data(channel_id)
            if channel_data:
                views = int(channel_data['YouTube Views'])
                subscribers = int(channel_data['YouTube Subscribers'])
                engagement_rate = (views / subscribers) * 100 if subscribers > 0 else 0
                content_frequency = calculate_content_frequency(channel_id)
                most_popular_video = get_most_popular_video(channel_id)
                channel_data['Most Common Category'] = category_name
                channel_data['Engagement Rate (%)'] = round(engagement_rate, 2)
                if content_frequency:
                    channel_data['Content Frequency'] = f"New content uploaded every {round(content_frequency, 2)} days"
                else:
                    channel_data['Content Frequency'] = "Not enough data to determine frequency"
                channel_data['Most Popular Video'] = most_popular_video or "No popular video found"
                comparison_data.append(channel_data)
    # Display
    print(f"\nChannel Data:\n")
    for channel in comparison_data:
        print(f"Handle: {channel['YouTube Handle']}")
        print(f"Channel Link: {channel['YouTube Channel Link']}")
        print(f"Subscribers: {channel['YouTube Subscribers']}")
        print(f"Views: {channel['YouTube Views']}")
        print(f"Videos: {channel['YouTube Videos']}")
        print(f"Engagement Rate: {channel['Engagement Rate (%)']}%")
        print(f"Overall Content Category: {channel['Most Common Category']}")
        print(f"Content Frequency: {channel['Content Frequency']}")
        print(f"Most Popular Video: {channel['Most Popular Video']}")
        print("-" * 50)

# ---------------------------
# Part 2 - Compare channels and visualize
# ---------------------------

def compare_multiple_channels_and_recommend_with_graph(channel_handles):
    """Compare multiple channels and visualize the comparison with graphs."""
    comparison_data = []
    for handle in channel_handles:
        channel_id = get_channel_id(handle)
        if not channel_id:
            continue
        channel_data = get_channel_data(channel_id)
        if channel_data:
            views = channel_data['YouTube Views']
            subscribers = channel_data['YouTube Subscribers']
            engagement_rate = (views / subscribers) * 100 if subscribers > 0 else 0
            engagement_rate = min(engagement_rate, 100)
            channel_data['Engagement Rate (%)'] = round(engagement_rate, 2)
            comparison_data.append(channel_data)
    if not comparison_data:
        print("No valid data found for any channel.")
        return
    # Sort
    comparison_data_sorted_by_subscribers = sorted(comparison_data, key=lambda x: x['YouTube Subscribers'], reverse=True)
    comparison_data_sorted_by_views = sorted(comparison_data, key=lambda x: x['YouTube Views'], reverse=True)
    comparison_data_sorted_by_engagement = sorted(comparison_data, key=lambda x: x['Engagement Rate (%)'], reverse=True)
    # Display
    print("\nChannel Comparison based on Subscribers:")
    for i, channel in enumerate(comparison_data_sorted_by_subscribers, 1):
        print(f"{i}. {channel['YouTube Handle']} - {locale.format_string('%d', channel['YouTube Subscribers'], grouping=True)} Subscribers")
    print("\nChannel Comparison based on Views:")
    for i, channel in enumerate(comparison_data_sorted_by_views, 1):
        print(f"{i}. {channel['YouTube Handle']} - {locale.format_string('%d', channel['YouTube Views'], grouping=True)} Views")
    print("\nChannel Comparison based on Engagement Rate:")
    for i, channel in enumerate(comparison_data_sorted_by_engagement, 1):
        print(f"{i}. {channel['YouTube Handle']} - {channel['Engagement Rate (%)']}% Engagement Rate")
    print("-" * 50)
    # Recommendation
    best_by_engagement = comparison_data_sorted_by_engagement[0]
    best_by_views = comparison_data_sorted_by_views[0]
    print("\n**Recommendation**:")
    print(f"Best Channel by Engagement Rate: {best_by_engagement['YouTube Handle']} with an engagement rate of {best_by_engagement['Engagement Rate (%)']}%")
    print(f"Best Channel by Views: {best_by_views['YouTube Handle']} with {locale.format_string('%d', best_by_views['YouTube Views'], grouping=True)} views")

# ---------------------------
# Part 3 - Recommend new channels based on others
# ---------------------------

def suggest_channel_based_on_others(channel_handles, youtube):
    """Suggest one new channel based on similarities with other channels you like."""
    suggested_channel = None
    input_channel_ids = []
    for handle in channel_handles:
        channel_id = get_channel_id(handle)
        if channel_id:
            input_channel_ids.append(channel_id)
    for channel_id in input_channel_ids:
        channel_data = get_channel_data(youtube, channel_id)
        if channel_data:
            search_request = youtube.search().list(part="snippet", type="channel", q=channel_data['YouTube Handle'], maxResults=10)
            search_response = search_request.execute()
            for item in search_response['items']:
                if item['snippet']['channelId'] not in input_channel_ids:
                    suggested_channel = item['snippet']
                    break
            if suggested_channel:
                break
    if suggested_channel:
        print("\nSuggested Channel Based on Your Preferences:\n")
        print(f"Channel Name: {suggested_channel['title']}")
        print(f"Channel Link: https://www.youtube.com/channel/{suggested_channel['channelId']}")
    else:
        print("No new similar channels found.")

# Part 1 - retrieves the information of the channel(s) entered

from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime

# Replace with your own API key
API_KEY = 'AIzaSyCXEhvGzLjh6IjRogjjJ3CJ2g4J9P64Yho'

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(handle, youtube):
    """Find the channel ID by channel handle using YouTube Search API."""
    try:
        request = youtube.search().list(
            part='snippet',
            q=handle,
            type='channel'
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['id']['channelId']
        return None
    except Exception as e:
        print(f"Error message: {e}")
        return None

def get_all_video_categories(channel_id, youtube, max_results=50):
    """Fetch a limited number of videos from the channel and return a list of categories."""
    categories = []
    try:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=max_results,
            type='video'
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['id']['videoId']
            video_request = youtube.videos().list(
                part='snippet',
                id=video_id
            )
            video_response = video_request.execute()
            if 'items' in video_response and len(video_response['items']) > 0:
                categories.append(video_response['items'][0]['snippet']['categoryId'])
        return categories
    except Exception as e:
        print(f"Error message: {e}")
        return categories

def get_category_name(category_id, youtube):
    """Fetch the category name from the category ID."""
    try:
        request = youtube.videoCategories().list(
            part='snippet',
            id=category_id
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        return None
    except Exception as e:
        print(f"Error message: {e}")
        return None

def get_channel_data(channel_id, youtube):
    """Fetch channel data from YouTube API."""
    try:
        request = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            channel_info = response['items'][0]
            return {
                'YouTube Handle': channel_info['snippet']['title'],
                'YouTube Channel Link': f"https://www.youtube.com/channel/{channel_id}",
                'YouTube Subscribers': int(channel_info['statistics'].get('subscriberCount', 0)),
                'YouTube Views': int(channel_info['statistics'].get('viewCount', 0)),
                'YouTube Videos': int(channel_info['statistics'].get('videoCount', 0))
            }
        return None
    except Exception as e:
        print(f"Error message: {e}")
        return None

def calculate_content_frequency(channel_id, youtube):
    """Calculate content upload frequency in days."""
    try:
        request = youtube.activities().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50
        )
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
        return None
    except Exception as e:
        print(f"Error message: {e}")
        return None

def get_most_popular_video(channel_id, youtube):
    """Get the most popular video for a given channel."""
    try:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=1,
            type='video',
            order='viewCount'
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            return f"{video['snippet']['title']} (https://www.youtube.com/watch?v={video['id']['videoId']})"
        return None
    except Exception as e:
        print(f"Error message: {e}")
        return None

def compare_channels(channel_handles, youtube):
    """Compare channels by retrieving categories and engagement rates."""
    comparison_data = []

    for handle in channel_handles:
        channel_id = get_channel_id(handle, youtube)
        if not channel_id:
            print(f"Handle not found: {handle}")
            continue

        categories = get_all_video_categories(channel_id, youtube)
        most_common_category = None
        if categories:
            most_common_category_id, _ = Counter(categories).most_common(1)[0]
            most_common_category = get_category_name(most_common_category_id, youtube)

        channel_data = get_channel_data(channel_id, youtube)
        if channel_data:
            views = channel_data['YouTube Views']
            subscribers = channel_data['YouTube Subscribers']
            engagement_rate = (views / subscribers) * 100 if subscribers > 0 else 0
            content_frequency = calculate_content_frequency(channel_id, youtube)
            most_popular_video = get_most_popular_video(channel_id, youtube)

            channel_data.update({
                'Most Common Category': most_common_category,
                'Engagement Rate (%)': round(engagement_rate, 2),
                'Content Frequency': f"New content every {round(content_frequency,2)} days" if content_frequency else "Not enough data",
                'Most Popular Video': most_popular_video or "No popular video found"
            })
            comparison_data.append(channel_data)

    return comparison_data

# Part 3 - suggest new channel based on other channels
def suggest_channel_based_on_others(channel_handles, youtube):
    suggested_channel = None
    input_channel_ids = [get_channel_id(handle, youtube) for handle in channel_handles if get_channel_id(handle, youtube)]
    
    for channel_id in input_channel_ids:
        channel_data = get_channel_data(channel_id, youtube)
        if not channel_data:
            continue
        search_request = youtube.search().list(
            part='snippet',
            type='channel',
            q=channel_data['YouTube Handle'],
            maxResults=10
        )
        search_response = search_request.execute()
        for item in search_response['items']:
            if item['snippet']['channelId'] not in input_channel_ids:
                suggested_channel = {
                    'Channel Name': item['snippet']['title'],
                    'Channel Link': f"https://www.youtube.com/channel/{item['snippet']['channelId']}"
                }
                break
        if suggested_channel:
            break
    return suggested_channel

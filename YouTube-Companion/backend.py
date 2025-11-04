# backend.py
from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime

API_KEY = 'AIzaSyCXEhvGzLjh6IjRogjjJ3CJ2g4J9P64Yho'
youtube = build('youtube', 'v3', developerKey=API_KEY)


# ------------------------------
# 1. Get Channel ID
# ------------------------------
def get_channel_id(handle):
    """Retrieve channel ID by handle or username."""
    try:
        # Try username first
        request = youtube.channels().list(part="id,snippet", forUsername=handle)
        response = request.execute()
        if response.get('items'):
            return response['items'][0]['id']
        # Fallback: search API
        search_request = youtube.search().list(part="snippet", q=handle, type="channel")
        search_response = search_request.execute()
        if search_response.get('items'):
            return search_response['items'][0]['id']['channelId']
    except Exception as e:
        print(f"Error getting channel ID for {handle}: {e}")
    return None


# ------------------------------
# 2. Get Channel Data
# ------------------------------
def get_channel_data(channel_id):
    """Return basic channel stats."""
    try:
        request = youtube.channels().list(part="snippet,statistics,contentDetails", id=channel_id)
        response = request.execute()
        if response.get('items'):
            ch = response['items'][0]
            return {
                'Handle': ch['snippet']['title'],
                'Link': f"https://www.youtube.com/channel/{channel_id}",
                'Subscribers': int(ch['statistics'].get('subscriberCount', 0)),
                'Views': int(ch['statistics'].get('viewCount', 0)),
                'Videos': int(ch['statistics'].get('videoCount', 0))
            }
    except Exception as e:
        print(f"Error getting channel data for {channel_id}: {e}")
    return None


# ------------------------------
# 3. Engagement Rate
# ------------------------------
def calculate_engagement_rate(channel_data):
    """Calculate views/subscribers * 100."""
    subs = channel_data['Subscribers']
    views = channel_data['Views']
    return round((views / subs * 100) if subs > 0 else 0, 2)


# ------------------------------
# 4. Video Categories
# ------------------------------
def get_all_video_categories(channel_id, max_results=50):
    """Fetch category IDs for a channel's videos."""
    categories = []
    try:
        request = youtube.search().list(
            part='snippet', channelId=channel_id, maxResults=max_results, type='video'
        )
        response = request.execute()
        for item in response.get('items', []):
            vid_id = item['id']['videoId']
            video_request = youtube.videos().list(part='snippet', id=vid_id)
            video_response = video_request.execute()
            if video_response.get('items'):
                categories.append(video_response['items'][0]['snippet']['categoryId'])
    except Exception as e:
        print(f"Error fetching video categories for {channel_id}: {e}")
    return categories


def get_category_name(category_id):
    """Convert category ID to name."""
    try:
        request = youtube.videoCategories().list(part='snippet', id=category_id)
        response = request.execute()
        if response.get('items'):
            return response['items'][0]['snippet']['title']
    except Exception as e:
        print(f"Error fetching category name {category_id}: {e}")
    return None


# ------------------------------
# 5. Content Frequency
# ------------------------------
def calculate_content_frequency(channel_id):
    """Average days between uploads."""
    try:
        request = youtube.activities().list(part='snippet,contentDetails', channelId=channel_id, maxResults=50)
        response = request.execute()
        dates = [datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
                 for item in response.get('items', []) if 'publishedAt' in item['snippet']]
        if len(dates) > 1:
            dates.sort(reverse=True)
            intervals = [(dates[i] - dates[i + 1]).days for i in range(len(dates)-1)]
            return round(sum(intervals) / len(intervals), 2)
    except Exception as e:
        print(f"Error calculating content frequency for {channel_id}: {e}")
    return None


# ------------------------------
# 6. Most Popular Video
# ------------------------------
def get_most_popular_video(channel_id):
    """Return the most viewed video title + link."""
    try:
        request = youtube.search().list(part='snippet', channelId=channel_id,
                                        maxResults=1, type='video', order='viewCount')
        response = request.execute()
        if response.get('items'):
            vid = response['items'][0]
            vid_id = vid['id']['videoId']
            title = vid['snippet']['title']
            return f"{title} (https://www.youtube.com/watch?v={vid_id})"
    except Exception as e:
        print(f"Error fetching most popular video for {channel_id}: {e}")
    return None


# ------------------------------
# 7. Compare Multiple Channels
# ------------------------------
def compare_channels(handles):
    """Return structured comparison data for multiple channels."""
    comparison = []
    for handle in handles:
        cid = get_channel_id(handle)
        if not cid:
            continue
        data = get_channel_data(cid)
        if not data:
            continue
        # Add engagement
        data['Engagement Rate (%)'] = calculate_engagement_rate(data)
        # Categories
        categories = get_all_video_categories(cid)
        if categories:
            most_common_id, _ = Counter(categories).most_common(1)[0]
            data['Most Common Category'] = get_category_name(most_common_id)
        else:
            data['Most Common Category'] = "N/A"
        # Content frequency
        freq = calculate_content_frequency(cid)
        data['Content Frequency (days)'] = freq if freq else "N/A"
        # Most popular video
        data['Most Popular Video'] = get_most_popular_video(cid) or "N/A"
        comparison.append(data)
    return comparison


# ------------------------------
# 8. Ranking & Best Channel
# ------------------------------
def rank_channels(data_list, key):
    return sorted(data_list, key=lambda x: x.get(key, 0), reverse=True)


def best_channel(data_list, key):
    ranked = rank_channels(data_list, key)
    return ranked[0] if ranked else None


# ------------------------------
# 9. Suggest New Channel
# ------------------------------
def suggest_channel_based_on_others(handles):
    """Suggest a new channel based on similarity with input channels."""
    suggested_channel = None
    input_ids = [get_channel_id(h) for h in handles if get_channel_id(h)]
    for cid in input_ids:
        ch_data = get_channel_data(cid)
        if not ch_data:
            continue
        try:
            request = youtube.search().list(part="snippet", type="channel",
                                            q=ch_data['Handle'], maxResults=10)
            response = request.execute()
            for item in response.get('items', []):
                if item['snippet']['channelId'] not in input_ids:
                    suggested_channel = {
                        'Handle': item['snippet']['title'],
                        'Link': f"https://www.youtube.com/channel/{item['snippet']['channelId']}"
                    }
                    break
            if suggested_channel:
                break
        except Exception as e:
            print(f"Error suggesting channel based on {ch_data['Handle']}: {e}")
    return suggested_channel

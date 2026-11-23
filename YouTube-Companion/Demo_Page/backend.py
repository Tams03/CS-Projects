import re
from collections import Counter
from datetime import datetime
from urllib.parse import unquote, urlsplit

CHANNEL_ID = re.compile(r"UC[A-Za-z0-9_-]{22}")
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com"}


def get_channel_id(value, youtube):
    value = value.strip()
    if not value:
        return None
    if re.match(r"^(?:https?://|(?:www\.|m\.)?youtube\.com/)", value, re.I):
        url = urlsplit(value if "://" in value else f"https://{value}")
        if url.hostname not in YOUTUBE_HOSTS:
            return None
        parts = unquote(url.path).strip("/").split("/")
        if parts[0].startswith("@"):
            value = parts[0]
        elif len(parts) >= 2 and parts[0] == "channel" and CHANNEL_ID.fullmatch(parts[1]):
            value = parts[1]
        else:
            return None

    if value.startswith("@") or CHANNEL_ID.fullmatch(value):
        selector = {"forHandle": value} if value.startswith("@") else {"id": value}
        items = youtube.channels().list(part="id", **selector).execute().get("items", [])
        return items[0]["id"] if items else None

    items = youtube.search().list(
        part="snippet", type="channel", q=value, maxResults=5
    ).execute().get("items", [])
    matches = {
        item["id"]["channelId"]
        for item in items
        if item["snippet"]["title"].casefold() == value.casefold()
    }
    return next(iter(matches)) if len(matches) == 1 else None


def _count(statistics, field):
    value = statistics.get(field)
    return int(value) if value is not None else None


def get_channel_data(channel_id, youtube):
    items = youtube.channels().list(
        part="snippet,statistics,contentDetails", id=channel_id
    ).execute().get("items", [])
    if not items:
        return None

    channel = items[0]
    stats = channel.get("statistics", {})
    subscribers = None if stats.get("hiddenSubscriberCount") else _count(stats, "subscriberCount")
    views = _count(stats, "viewCount")
    result = {
        "YouTube Handle": channel["snippet"]["title"],
        "YouTube Channel Link": f"https://www.youtube.com/channel/{channel_id}",
        "YouTube Subscribers": subscribers,
        "YouTube Views": views,
        "YouTube Videos": _count(stats, "videoCount"),
        "Views per subscriber": round(views / subscribers, 2) if subscribers and views is not None else None,
        "Most Common Category": None,
        "Content Frequency": None,
        "Most Popular Video": None,
    }
    uploads = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    if not uploads:
        return result

    playlist = youtube.playlistItems().list(
        part="contentDetails", playlistId=uploads, maxResults=50
    ).execute().get("items", [])
    ids = list(dict.fromkeys(item["contentDetails"]["videoId"] for item in playlist))
    if not ids:
        return result

    videos = youtube.videos().list(
        part="snippet,statistics", id=",".join(ids)
    ).execute().get("items", [])
    snippets = [video["snippet"] for video in videos]
    categories = Counter(s["categoryId"] for s in snippets if s.get("categoryId"))
    if categories:
        category_id = categories.most_common(1)[0][0]
        labels = youtube.videoCategories().list(
            part="snippet", id=category_id
        ).execute().get("items", [])
        if labels:
            result["Most Common Category"] = labels[0]["snippet"]["title"]

    dates = sorted(datetime.fromisoformat(s["publishedAt"].replace("Z", "+00:00"))
                   for s in snippets if s.get("publishedAt"))
    if len(dates) > 1:
        days = (dates[-1] - dates[0]).total_seconds() / 86400 / (len(dates) - 1)
        result["Content Frequency"] = f"{days:.2f} days between sampled uploads"

    ranked = [v for v in videos if v.get("statistics", {}).get("viewCount") is not None]
    if ranked:
        top = max(ranked, key=lambda v: int(v["statistics"]["viewCount"]))
        result["Most Popular Video"] = f"{top['snippet']['title']} (https://www.youtube.com/watch?v={top['id']})"
    return result


def compare_channels(channel_handles, youtube):
    results = []
    seen = set()
    for handle in channel_handles:
        channel_id = get_channel_id(handle, youtube)
        if channel_id and channel_id not in seen:
            seen.add(channel_id)
            data = get_channel_data(channel_id, youtube)
            if data:
                results.append(data)
    return results


def suggest_channel_based_on_others(channel_handles, youtube):
    ids = list(dict.fromkeys(
        channel_id for handle in channel_handles
        if (channel_id := get_channel_id(handle, youtube))
    ))
    if not ids:
        return None
    seeds = youtube.channels().list(part="snippet", id=",".join(ids)).execute().get("items", [])
    for seed in seeds:
        items = youtube.search().list(
            part="snippet", type="channel", q=seed["snippet"]["title"], maxResults=10
        ).execute().get("items", [])
        for item in items:
            candidate = item["id"]["channelId"]
            if candidate not in ids:
                return {
                    "Channel Name": item["snippet"]["title"],
                    "Channel Link": f"https://www.youtube.com/channel/{candidate}",
                }
    return None

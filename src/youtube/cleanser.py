from typing import Dict, Any


def parser(data: Dict) -> Dict[str, Any]:
    items = data["items"][0]
    snippet = items["snippet"]
    statistics = items["statistics"]

    return {
        "channel_id": items["id"],
        "title": snippet["title"],
        "description": snippet["description"],
        "custom_url": snippet["customUrl"],
        "published_at": snippet["publishedAt"],
        "thumbnail_url": snippet["thumbnails"]["high"]["url"],
        "view_count": statistics["viewCount"],
        "subscriber_count": statistics["subscriberCount"],
        "video_count": statistics["videoCount"]
    }


def save_to_db(data: Dict) -> None:
    ...


if __name__ == "__main__":
    ...

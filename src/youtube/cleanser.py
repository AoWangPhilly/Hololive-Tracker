from typing import Dict, Any

from src.database import Session
from src.models import RawYouTubeMetric, CleansedYouTubeMetric, RawTwitterMetric


def parse_data(data: Dict) -> Dict[str, Any]:
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


def save_to_db(row_data: RawTwitterMetric) -> None:
    cleansed_metric = parse_data(row_data.data)
    session = Session()
    youtube_metric = CleansedYouTubeMetric(**cleansed_metric, raw_json_id=row_data.id)
    session.add(youtube_metric)
    session.commit()


if __name__ == "__main__":
    session = Session()
    result = session.query(RawYouTubeMetric).first()
    save_to_db(result)

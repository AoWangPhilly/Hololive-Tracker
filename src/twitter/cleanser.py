from datetime import timezone
from pprint import pprint
from typing import Dict, Any, List

from src import models
from src.database import Session


def parse_data(user: Dict) -> Dict[str, Any]:
    public_metrics = user["public_metrics"]
    youtube_channel_id = None

    output = {
        "twitter_id": user["id"],
        "username": user["username"],
        "name": user["name"],
        "profile_image_url": user["profile_image_url"],
        "created_at": user["created_at"],
        "description": user["description"],
        "followers_count": public_metrics["followers_count"],
        "following_count": public_metrics["following_count"],
        "tweet_count": public_metrics["tweet_count"],
        "listed_count": public_metrics["listed_count"]
    }
    if entities := user.get("entities"):
        urls = entities["url"]["urls"]
        for url in urls:
            if "youtube" in url["expanded_url"]:
                expanded_url = url["expanded_url"]
                base_url, channel_id = expanded_url.rsplit("/", 1)
                youtube_channel_id = channel_id
                break

    output["youtube_channel_id"] = youtube_channel_id
    return output


def save_to_db(row_data: List[models.RawMetric]) -> None:
    session = Session()
    for data in row_data:
        datetime = data.datetime
        unix_id = datetime.replace(tzinfo=timezone.utc).timestamp()
        metrics = data.data["data"]
        for metric in metrics:
            cleansed_data = parse_data(user=metric)
            cleansed_data["unix_id"] = unix_id
            pprint(cleansed_data)
            cleansed_metric = models.CleansedMetric(**cleansed_data)
            session.add(cleansed_metric)
            session.commit()


if __name__ == "__main__":
    session = Session()

    result = session.query(models.RawMetric).all()
    # save_to_db(result)
    # print(result[0].datetime)
    # pprint(parse_data(result[0].data["data"][0]))

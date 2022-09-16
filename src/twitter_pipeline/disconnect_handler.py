import datetime
from dataclasses import dataclass
from typing import Dict, List, Callable, Union

import requests
from decouple import config

from src.twitter_pipeline.constants import (TWEET_FIELDS, EXPANSIONS, MEDIA_FIELDS, POLL_FIELDS,
                                            USER_FIELDS, PLACE_FIELDS, EN_TWITTER_ID)
from src.twitter_pipeline.database import save_to_db

bearer_token = config("bearer_token")


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def get_request(url: str, params: Dict, auth: Callable = bearer_oauth) -> Union[Dict, None]:
    response = requests.get(url=url, auth=auth, params=params)
    if not response.ok:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )

    return response.json()


@dataclass
class StreamDisconnectHandler:
    connection_break_time: Union[datetime.datetime, None] = None
    connection_reconnect_time: Union[datetime.datetime, None] = None

    def get_timeline_for_user(self, twitter_id: int, max_results: int = 100) -> List[Dict]:
        params = {
            "max_results": max_results,
            "start_time": self.connection_break_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_time": self.connection_reconnect_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tweet.fields": ",".join(TWEET_FIELDS),
            "expansions": ",".join(EXPANSIONS),
            "media.fields": ",".join(MEDIA_FIELDS),
            "poll.fields": ",".join(POLL_FIELDS),
            "user.fields": ",".join(USER_FIELDS),
            "place.fields": ",".join(PLACE_FIELDS)
        }

        url = f"https://api.twitter.com/2/users/{twitter_id}/tweets"

        json_ = get_request(url=url, params=params)

        output = [{"data": data} for data in json_["data"]]

        while pagination_token := json_["meta"].get("next_token", None):
            params["pagination_token"] = pagination_token
            json_ = get_request(url=url, params=params)
            output.extend([{"data": data} for data in json_["data"]])

        return output

    def get_timeline_for_users(self, twitter_ids: List[int]) -> List[Dict]:
        output = []
        for twitter_id in twitter_ids:
            output.extend(self.get_timeline_for_user(twitter_id=twitter_id))
        return output

    def save_missing_tweets_to_db(self):
        missing_tweets = self.get_timeline_for_users(twitter_ids=EN_TWITTER_ID)
        for tweet in missing_tweets:
            save_to_db(data=tweet)

    def reset(self):
        self.connection_reconnect_time = None
        self.connection_break_time = None


if __name__ == "__main__":
    start_time = datetime.datetime(year=2022, month=9, day=13)
    end_time = datetime.datetime(year=2022, month=9, day=17)
    handler = StreamDisconnectHandler(start_time, end_time)
    print(handler.save_missing_tweets_to_db())

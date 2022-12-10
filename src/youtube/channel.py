from typing import Dict

import requests
from decouple import config

from src.constants import EN_YOUTUBE_CHANNEL_ID

YOUTUBE_API_KEY = config("YOUTUBE_API_KEY")
BASE_URL = "https://youtube.googleapis.com/youtube/v3/channels"
PARTS = "snippet,contentDetails,statistics"


class Channel:
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id

    def set_channel_id(self, channel_id: str) -> None:
        self.channel_id = channel_id

    def get_channel_id(self) -> str:
        return self.channel_id

    def _build_url(self) -> str:
        return f"{BASE_URL}?part={PARTS}&id={self.channel_id}&key={YOUTUBE_API_KEY}"

    def call_endpoint(self) -> Dict:
        url = self._build_url()
        response = requests.get(url)
        if not response.ok:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        return response.json()

    def save_to_db(self) -> None:
        ...


if __name__ == "__main__":
    first = EN_YOUTUBE_CHANNEL_ID[0]
    channel = Channel(channel_id=first)
    print(channel.call_endpoint())

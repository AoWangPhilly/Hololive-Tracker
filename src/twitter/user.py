from typing import List, Union, Dict

import requests
from decouple import config

from src.api.base import API
from src.constants import USER_FIELDS, EN_TWITTER_ID
from src.models import RawTwitterMetric

BASE_URL = "https://api.twitter.com/2/users"


class User(API):
    def __init__(self, ids: Union[int, List[int]]) -> None:
        self.ids = ids

    def _build_url(self) -> str:
        ids = ",".join(map(str, self.ids)) if type(self.ids) == list else self.ids
        user_fields = ",".join(USER_FIELDS)
        return f"{BASE_URL}?ids={ids}&user.fields={user_fields}"

    def call_endpoint(self) -> Dict:
        url = self._build_url()
        response = requests.get(url, headers={"Authorization": f'Bearer {config("bearer_token")}'})
        if not response.ok:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        return response.json()


if __name__ == "__main__":
    users = User(ids=EN_TWITTER_ID)
    users.save_to_db(table=RawTwitterMetric)

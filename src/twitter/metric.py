# https://api.twitter.com/2/users?ids=1283653858510598144&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld

from typing import List, Union

import requests
from decouple import config

from constants import USER_FIELDS, EN_TWITTER_ID

BASE_URL = "https://api.twitter.com/2/users"


class User:
    def __init__(self, ids: Union[int, List[int]]) -> None:
        self.ids = ids

    def _build_url(self) -> str:
        ids = ",".join(map(str, self.ids)) if type(self.ids) == list else self.ids
        user_fields = ",".join(USER_FIELDS)
        return f"{BASE_URL}?ids={ids}&user.fields={user_fields}"

    def call_endpoint(self):
        url = self._build_url()
        response = requests.get(url, headers={"Authorization": f'Bearer {config("bearer_token")}'})
        if not response.ok:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        return response.json()


if __name__ == "__main__":
    users = User(ids=EN_TWITTER_ID)
    print(users.call_endpoint())

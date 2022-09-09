import os

from constants import TWEET_FIELDS, EXPANSIONS, MEDIA_FIELDS, POLL_FIELDS, USER_FIELDS, PLACE_FIELDS
from hololive_stream import HololiveStreamingClient

BEARER_TOKEN = os.environ.get("bearer_token")


def main():
    client = HololiveStreamingClient(bearer_token=BEARER_TOKEN)
    client.filter(tweet_fields=TWEET_FIELDS, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS,
                  poll_fields=POLL_FIELDS, user_fields=USER_FIELDS, place_fields=PLACE_FIELDS)


if __name__ == "__main__":
    main()

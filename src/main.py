import json
import os
from pprint import pprint

from tweepy import StreamingClient, StreamRule

from constants import EN_MYTH_TWITTER_ID, EN_VSINGER_TWITTER_ID, EN_COUNCIL_TWITTER_ID, EN_TEMPUS_TWITTER_ID, \
    TWEET_FIELDS, EXPANSIONS, MEDIA_FIELDS, POLL_FIELDS, USER_FIELDS, PLACE_FIELDS

BEARER_TOKEN = os.environ.get("bearer_token")


def create_rule() -> StreamRule:
    twitter_ids = EN_MYTH_TWITTER_ID + EN_VSINGER_TWITTER_ID + EN_COUNCIL_TWITTER_ID + EN_TEMPUS_TWITTER_ID
    rule_value = " OR ".join([f"from:{twitter_id}" for twitter_id in twitter_ids])
    return StreamRule(value=rule_value)


def delete_rule(client: StreamingClient) -> None:
    if rule_data := client.get_rules().data:
        current_rules = list(map(lambda rule: rule.id, rule_data))
        client.delete_rules(current_rules)


def add_rule(client: StreamingClient) -> None:
    rules = create_rule()
    client.add_rules(rules)


class HololiveStreamingClient(StreamingClient):
    def on_connect(self) -> None:
        print("Stream connected! :)")

    def on_data(self, raw_data) -> None:
        pprint(json.loads(raw_data))
        print("\n")

    def on_exception(self, exception: Exception) -> None:
        print("An exception has occurred")
        print(f"{exception=}")

    def on_connection_error(self) -> None:
        print("A streaming connection has occurred! Or stream has timed out!")

    def on_disconnect(self) -> None:
        print("Stream disconnected! Good bye!")


def main():
    client = HololiveStreamingClient(bearer_token=BEARER_TOKEN)
    delete_rule(client)
    add_rule(client)

    client.filter(tweet_fields=TWEET_FIELDS, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, poll_fields=POLL_FIELDS,
                  user_fields=USER_FIELDS, place_fields=PLACE_FIELDS)


if __name__ == "__main__":
    main()

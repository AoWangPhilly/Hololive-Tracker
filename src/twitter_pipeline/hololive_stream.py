import json
from pprint import pprint

from tweepy import StreamingClient, StreamRule

from constants import EN_MYTH_TWITTER_ID, EN_VSINGER_TWITTER_ID, EN_COUNCIL_TWITTER_ID, EN_TEMPUS_TWITTER_ID


def create_rules() -> StreamRule:
    twitter_ids = EN_MYTH_TWITTER_ID + EN_VSINGER_TWITTER_ID + EN_COUNCIL_TWITTER_ID + EN_TEMPUS_TWITTER_ID
    rule_value = " OR ".join([f"from:{twitter_id}" for twitter_id in twitter_ids])
    return StreamRule(value=rule_value)


class HololiveStreamingClient(StreamingClient):

    def _add_rule(self) -> None:
        rules = create_rules()
        self.add_rules(add=rules)

    def _delete_rule(self) -> None:
        if rule_data := self.get_rules().data:
            current_rules = list(map(lambda rule: rule.id, rule_data))
            self.delete_rules(ids=current_rules)

    def on_connect(self) -> None:
        self._add_rule()
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
        self._delete_rule()
        print("Stream disconnected! Good bye!")

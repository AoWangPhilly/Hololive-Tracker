import json
from pprint import pprint
from typing import Union

from tweepy import StreamingClient, StreamRule

from constants import EN_TWITTER_ID
from database import save_to_db


def create_rules() -> StreamRule:
    rule_value = " OR ".join([f"from:{twitter_id}" for twitter_id in EN_TWITTER_ID])
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

    def on_data(self, raw_data: Union[str, bytes]) -> None:
        data = json.loads(raw_data)
        save_to_db(data=data)
        pprint(data)
        print("\n")

    def on_exception(self, exception: Exception) -> None:
        print("An exception has occurred")
        print(f"{exception=}")

    def on_connection_error(self) -> None:
        print("A streaming connection has occurred! Or stream has timed out!")

    def on_disconnect(self) -> None:
        self._delete_rule()
        print("Stream disconnected! Good bye!")

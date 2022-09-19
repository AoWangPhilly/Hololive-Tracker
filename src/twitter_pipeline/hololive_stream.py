import asyncio
import datetime
import json
import logging
from pprint import pprint
from typing import Union

from tweepy import StreamingClient, StreamRule

from src.discord_bot.web_hook import send_message
from src.twitter_pipeline.constants import EN_TWITTER_ID
from src.twitter_pipeline.database import save_to_db
from src.twitter_pipeline.disconnect_handler import StreamDisconnectHandler


def set_logger() -> None:
    """Create logger to check stream connections
    :return: None
    """
    logging.basicConfig(
        filename="twitter_stream.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filemode="w",
    )
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


def create_rules() -> StreamRule:
    """Creates a rule string for which accounts to get real-time tweets from
    :return: A tweepy StreamRule object
    """
    rule_value = " OR ".join([f"from:{twitter_id}" for twitter_id in EN_TWITTER_ID])
    return StreamRule(value=rule_value)


class HololiveStreamingClient(StreamingClient):
    def __init__(self, bearer_token, **kwargs):
        super().__init__(bearer_token, **kwargs)
        self.disconnect_handler = StreamDisconnectHandler()

    def _add_rule(self) -> None:
        rules = create_rules()
        self.add_rules(add=rules)

    def _delete_rule(self) -> None:
        if rule_data := self.get_rules().data:
            current_rules = list(map(lambda rule: rule.id, rule_data))
            self.delete_rules(ids=current_rules)

    def on_connect(self) -> None:
        set_logger()
        self._add_rule()
        print("Stream connected! :)")
        try:
            if self.disconnect_handler.connection_break_time:
                self.disconnect_handler.connection_reconnect_time = datetime.datetime.now()
                self.disconnect_handler.save_missing_tweets_to_db()
                self.disconnect_handler.reset()
        except Exception as e:
            logging.critical(f"Critical: {e}")

    def on_data(self, raw_data: Union[str, bytes]) -> None:
        data = json.loads(raw_data)

        save_to_db(data=data)

        asyncio.run(send_message(json_=data))

        pprint(data)
        print("\n")

    def on_exception(self, exception: Exception) -> None:
        print("An exception has occurred")
        print(f"{exception=}")

    def on_connection_error(self) -> None:
        print("A streaming connection has occurred! Or stream has timed out!")
        self.disconnect_handler.connection_break_time = datetime.datetime.now()

    def on_disconnect(self) -> None:
        self._delete_rule()
        print("Stream disconnected! Good bye!")

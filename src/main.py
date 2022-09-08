import os

from tweepy import StreamingClient, StreamRule

from constants import EN_MYTH_TWITTER_ID, EN_VSINGER_TWITTER_ID, EN_COUNCIL_TWITTER_ID, EN_TEMPUS_TWITTER_ID

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


def main():
    client = StreamingClient(bearer_token=BEARER_TOKEN)
    delete_rule(client)
    add_rule(client)


if __name__ == "__main__":
    main()

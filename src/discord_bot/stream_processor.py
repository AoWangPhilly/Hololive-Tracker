from typing import Dict
from typing import Tuple

from decouple import config
from tweepy import Client
from tweepy import Tweet, User, Media

from src.twitter_pipeline.constants import (TWEET_FIELDS, EXPANSIONS, PLACE_FIELDS, USER_FIELDS, POLL_FIELDS,
                                            MEDIA_FIELDS)

bearer_token = config("bearer_token")
client = Client(bearer_token=bearer_token)


def process_stream(json_: Dict) -> Tuple[str, Dict]:
    output = {}
    tweet_data = Tweet(json_["data"])

    if tweet_data.referenced_tweets is None:
        output["tweet_id"] = tweet_data.id
        output["conversation_id"] = tweet_data.id
        output["author_id"] = tweet_data.author_id
        output["text"] = tweet_data.text
        output["created_at"] = tweet_data.created_at

        includes = json_["includes"]
        user = User(includes["users"][0])
        output["name"] = user.name
        output["profile_url"] = f"https://twitter.com/{user.username}"
        output["username"] = user.username
        output["profile_image_url"] = user.profile_image_url
        if includes.get("media", None):
            media = Media(includes["media"][0])
            output["image_url"] = media.url
        return "tweet", output

    elif tweet_data.referenced_tweets[0].type == "retweeted":
        output["tweet_id"] = tweet_data.id
        output["conversation_id"] = tweet_data.id
        includes = json_["includes"]
        for data in includes["users"]:
            user = User(data=data)
            if int(tweet_data.author_id) == user.id:
                output["retweeter_name"] = user.name
                output["retweeter_profile_url"] = user.url
                output["retweeter_username"] = user.username
                output["retweeter_profile_image_url"] = user.profile_image_url

        original_tweet_id = includes["tweets"][0]["id"]
        original_tweet = client.get_tweet(id=original_tweet_id, tweet_fields=TWEET_FIELDS,
                                          expansions=EXPANSIONS, media_fields=MEDIA_FIELDS,
                                          poll_fields=POLL_FIELDS, user_fields=USER_FIELDS, place_fields=PLACE_FIELDS)
        output["text"] = original_tweet.data.text
        output["created_at"] = original_tweet.data.created_at
        includes = original_tweet.includes
        original_poster = includes["users"][0]
        output["name"] = original_poster.name
        output["profile_url"] = f"https://twitter.com/{original_poster.username}"
        output["username"] = original_poster.username
        output["profile_image_url"] = original_poster.profile_image_url

        if includes.get("media", None):
            media = includes["media"][0]
            output["image_url"] = media.url if media.url else media.preview_image_url

        return "retweet", output

    elif tweet_data.referenced_tweets[0].type == "quoted":
        output["tweet_id"] = tweet_data.id
        output["text"] = tweet_data.text
        output["author_id"] = tweet_data.author_id
        output["conversation_id"] = tweet_data.conversation_id
        output["created_at"] = tweet_data.created_at

        includes = json_["includes"]
        if includes.get("media", None):
            media = Media(includes["media"][0])
            output["image_url"] = media.url

        for data in includes["users"]:
            user = User(data=data)
            if int(tweet_data.author_id) == user.id:
                output["name"] = user.name
                output["profile_url"] = user.url
                output["username"] = user.username
                output["profile_image_url"] = user.profile_image_url

        quoted_tweet_id = includes["tweets"][0]["id"]
        original_tweet = client.get_tweet(id=quoted_tweet_id, tweet_fields=TWEET_FIELDS,
                                          expansions=EXPANSIONS, media_fields=MEDIA_FIELDS,
                                          poll_fields=POLL_FIELDS, user_fields=USER_FIELDS, place_fields=PLACE_FIELDS)
        output["quoted_text"] = original_tweet.data.text
        output["quoted_created_at"] = original_tweet.data.created_at
        includes = original_tweet.includes
        original_poster = includes["users"][0]
        output["quoted_name"] = original_poster.name
        output["quoted_profile_url"] = f"https://twitter.com/{original_poster.username}"
        output["quoted_username"] = original_poster.username
        output["quoted_profile_image_url"] = original_poster.profile_image_url

        if includes.get("media", None):
            media = includes["media"][0]
            output["quoted_image_url"] = media.url if media.url else media.preview_image_url

        return "quoted", output

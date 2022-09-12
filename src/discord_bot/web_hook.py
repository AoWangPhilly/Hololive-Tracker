import datetime
import os
from typing import Dict

import aiohttp
from discord import Embed, Webhook


def parse_stream_data(json_) -> Dict:
    output = {}
    data = json_["data"]
    includes = json_["includes"]
    output["created_at"] = data["created_at"]
    output["text"] = data["text"]
    output["author_id"] = data["author_id"]
    output["conversation_id"] = data["conversation_id"]
    for user in includes["users"]:
        if user["id"] == output["author_id"]:
            output["name"] = user["name"]
            output["profile_image_url"] = user["profile_image_url"]
            output["username"] = user["username"]

    output["twitter_post_url"] = f"https://twitter.com/{output['username']}/status/{output['conversation_id']}"
    if ref_tweet := data.get("referenced_tweets", None):
        output["tweet_type"] = ref_tweet[0]["type"]
    else:
        output["tweet_type"] = "original"
    return output


def create_embed(post_data: Dict) -> Embed:
    name = f'{post_data["name"]} @({post_data["username"]})'
    url = f'https://twitter.com/{post_data["username"]}'
    icon_url = post_data["profile_image_url"]
    description = post_data["text"]
    date_posted = datetime.datetime.strptime(post_data["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    footer_text = f"Powered by Hololive-Tracker • {date_posted.date()}"

    embed = Embed(description=description)
    embed.set_author(name=name, url=url, icon_url=icon_url)
    embed.set_footer(text=footer_text, icon_url="hololive-logo.png")
    return embed


async def send_message(data: Dict) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.environ.get("twitter_webhook_url"), session=session)
        data_ = parse_stream_data(data)
        username = f'{data_["name"]} • Hololive-Tracker'
        if data_["tweet_type"] == "original":
            await webhook.send(f'[Tweeted]({data_["twitter_post_url"]})',
                               embed=create_embed(post_data=data_), username=username)

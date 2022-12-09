from typing import Dict, Sequence, Union

import aiohttp
from decouple import config
from discord import Embed
from discord import Webhook

from src.discord_bot.stream_processor import process_stream


def create_embed(tweet_type: str, info: Dict) -> Union[Embed, Sequence[Embed]]:
    embed = Embed(description=info["text"], timestamp=info["created_at"])
    embed.set_author(name=f"{info['name']} (@{info['username']})", url=info["profile_url"],
                     icon_url=info["profile_image_url"])
    embed.set_footer(text="Powered by Hololive-Tracker",
                     icon_url="https://tweetshift.com/static/images/profile.png")

    if image_url := info.get("image_url", None):
        embed.set_image(url=image_url)

    if tweet_type == "quoted":
        quoted_embed = Embed(description=info["quoted_text"], timestamp=info["quoted_created_at"])
        quoted_embed.set_author(name=f"{info['quoted_name']} (@{info['quoted_username']})",
                                url=info["quoted_profile_url"],
                                icon_url=info["quoted_profile_image_url"])
        quoted_embed.set_footer(text="Powered by Hololive-Tracker",
                                icon_url="https://tweetshift.com/static/images/profile.png")

        if image_url := info.get("quoted_image_url", None):
            quoted_embed.set_image(url=image_url)

        return embed, quoted_embed

    return embed


async def send_message(json_: Dict) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config("twitter_webhook_url"), session=session)
        tweet_type, data = process_stream(json_)
        if tweet_type == "tweet":
            embed = create_embed(tweet_type=tweet_type, info=data)

            await webhook.send(f'[Tweeted](https://twitter.com/{data["username"]}/status/{data["tweet_id"]})',
                               embed=embed,
                               avatar_url=data["profile_image_url"], username=f"{data['name']} • Hololive-Tracker")
        elif tweet_type == "retweet":
            embed = create_embed(tweet_type=tweet_type, info=data)

            await webhook.send(
                f'[Retweeted @{data["username"]} ...](https://twitter.com/{data["retweeter_username"]}/status/{data["tweet_id"]})',
                embed=embed,
                avatar_url=data["retweeter_profile_image_url"], username=f"{data['retweeter_name']} • Hololive-Tracker")

        elif tweet_type == "quoted":
            embed = create_embed(tweet_type=tweet_type, info=data)

            await webhook.send(
                f'[Quoted @{data["quoted_username"]} ...](https://twitter.com/{data["username"]}/status/{data["tweet_id"]})',
                embeds=embed,
                avatar_url=data["profile_image_url"], username=f"{data['name']} • Hololive-Tracker")

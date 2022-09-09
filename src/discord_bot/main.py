import asyncio
import os

import aiohttp
from discord import Webhook


async def foo():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.environ.get("twitter_webhook_url"), session=session)
        await webhook.send('[Tweeted](https://twitter.com/regisaltare/status/1568244295626276868)', username='Foo')


def main() -> None:
    asyncio.run(foo())


if __name__ == "__main__":
    main()

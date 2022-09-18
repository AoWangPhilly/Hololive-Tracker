import asyncio
import json

from src.discord_bot.web_hook import send_message


def main() -> None:
    with open("src/discord_bot/example.json", "r") as f:
        a = json.loads(f.read())
        asyncio.run(send_message(a))


if __name__ == "__main__":
    main()

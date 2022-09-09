import json
from pprint import pprint
from typing import Dict


def create_discord_message(json_) -> Dict:
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
    return output


if __name__ == "__main__":
    with open("example.json", 'r') as j:
        contents = json.loads(j.read())
    pprint(create_discord_message(contents))

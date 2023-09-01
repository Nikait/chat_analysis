import yaml
import json
import asyncio
from telethon import TelegramClient

from data_arragment import parse_by_users, user_data


async def main(client: TelegramClient, config: dict[str, str | int]) -> None:
    channel = await client.get_entity(config["group_name"])
    messages = await client.get_messages(channel, limit=config["limit"])
    user_list = client.iter_participants(entity=config["group_name"])
    data = await user_data(user_list)
    users, statistics = data
    print(statistics)
    ordered_data = parse_by_users(messages, users)
    
    with open(f'{config["group_name"]}_result.json', 'w') as fp:
        json.dump(ordered_data, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])
    client.start()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(client, config))
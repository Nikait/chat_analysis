import asyncstdlib as alib
from collections import defaultdict
from typing import DefaultDict

from telethon.tl.custom import Dialog
from telethon.client.chats import _ParticipantsIter


async def user_data(data: _ParticipantsIter) -> tuple[DefaultDict, dict]:
    """
    collection of information about users
    """
    user_data_base = defaultdict(dict)
    fields = ["premium", "scam", "first_name", "last_name", "username", "phone"]

    statistics = {
        "users_amount" : 0,
        "premium" : 0,
        "scam": 0,
        "phone" : 0,
    }

    async for ind, user in alib.enumerate(data):
        for field in fields:
            user_data_base[user.id][field] = user.to_dict()[field]
            user_data_base[user.id]["messages"] = ""
            if field in statistics.keys() and user.to_dict()[field]:
                statistics[field] += 1

        statistics["len"] = ind

    return user_data_base, statistics



def parse_by_users(messages: Dialog, users: DefaultDict[str, dict]) -> DefaultDict[str, dict]:
    """
    mapping all messages to their authors
    """
    _users = users
    for message in messages:
        identity, text = message.sender_id, message.message
        if "messages" in _users[identity] and message.message is not None:
            _users[identity]["messages"] += f" {message.message}."

    return _users
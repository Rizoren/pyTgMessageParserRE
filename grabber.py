from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest


def flat(obj, key=''):
    if type(obj) == dict:
        key = key + '_' if key else key
        for k in obj:
            yield from flat(obj[k], key + str(k))
    else:
        yield key, obj


def convert(msg, target_keys):
    flat_msg = {k: v for k, v in flat(msg)}
    if set(target_keys.keys()).issubset(flat_msg.keys()):
        return {target_keys[i]: flat_msg[i] for i in target_keys.keys()}
    else:
        return None


class GrabberTg:

    client = None

    def client_init(self, api_id, api_hash, username):
        self.client = TelegramClient(username, api_id, api_hash)

    def client_start(self):
        self.client.start()

    async def dump_all_messages(self, channel, msg_dto):
        offset_msg = 0 
        limit_msg = 100 
        total_messages = 0
        total_count_limit = 0
        all_messages = []

        while True:
            history = await self.client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                message_dto = convert(message.to_dict(), msg_dto)
                if message_dto is not None:
                    all_messages.append(message_dto)
            offset_msg = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        return all_messages

    def get_messages(self, name_channel, msg_dto):
        channel = self.client.get_entity(name_channel)
        with self.client:
            result = self.client.loop.run_until_complete(self.dump_all_messages(channel, msg_dto))
        return result

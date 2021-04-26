import sys

from telethon.sync import TelegramClient
from telethon import functions


if len(sys.argv) == 2:
    order_id = sys.argv[1]
else:
    sys.exit(0)

api_id = 5177145
api_hash = 'b62cd3362a6e7f553887cf0e3bbffaf8'

with TelegramClient('session_name', api_id, api_hash) as client:
    # bot_id = 1531692979
    # bot_id = 1480198758
    bot_id = 'StudyExchangeBot'
    result = client(functions.messages.CreateChatRequest(users=[bot_id], title='Заказ #{}'.format(order_id)))
    chat_id = result.chats[0].id
    client(functions.messages.EditChatAdminRequest(chat_id=chat_id, user_id=bot_id, is_admin=True))
    client(functions.messages.SendMessageRequest(peer=chat_id, message='/create_chat {}'.format(order_id)))

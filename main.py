from pprint import pprint

from telegram import Bot, BotCommand, ParseMode
from telegram.ext import Updater, Defaults
import logging

from command_handler import command_handler
from user_panel import *

with db_session:
    TOKEN = Settings.get(key='tg_token').value

bot = Bot(token=TOKEN)

commands = []

# commands = [
#     BotCommand(command='/start',  description='Начать работу с ботом'),
#     BotCommand(command="/menu", description="Список комманд"),
#     BotCommand(command="/myprofile", description="Мой профиль"),
#     BotCommand(command="/profile", description="Профиль исполнителя"),
#     BotCommand(command="/balance", description="Управление балансом"),
#     BotCommand(command="/neworder", description="Сделать заказ"),
#     BotCommand(command="/myorders", description="Посмотреть свои заказы"),
#     BotCommand(command="/order", description="Посмотреть определенный заказ"),
# ]

bot.set_my_commands(commands)

# defaults = Defaults(parse_mode=ParseMode.HTML)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

command_handler(dispatcher)

updater.start_polling()

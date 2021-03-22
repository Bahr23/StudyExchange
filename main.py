from telegram.ext import Updater, Defaults
import logging

from command_handler import command_handler
from user_panel import *


commands = []

bot.set_my_commands(commands)

# defaults = Defaults(parse_mode=ParseMode.HTML)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

command_handler(dispatcher)

updater.start_polling()
os.system('python payment.py')

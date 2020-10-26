from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from user_panel import *
from admin_panel import *
from chat_panel import *
from button import *


def command_handler(dispatcher):
    # User commands
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))

    dispatcher.add_handler(CommandHandler("profile", profile))
    dispatcher.add_handler(CommandHandler("myprofile", myprofile))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("menu", menu))

    dispatcher.add_handler(CommandHandler("order", order))
    dispatcher.add_handler(CommandHandler("neworder", new_order))
    dispatcher.add_handler(CommandHandler("myorders", my_orders))
    dispatcher.add_handler(CommandHandler("delorder", del_order))


    # Chat
    dispatcher.add_handler(CommandHandler("chat", chat))
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(CommandHandler("done", done))


    # Admin commands
    dispatcher.add_handler(CommandHandler("channel", channel))
    dispatcher.add_handler(CommandHandler("adminpanel", adminpanel))
    dispatcher.add_handler(CommandHandler("user", user))
    dispatcher.add_handler(CommandHandler("getorder", getorder))
    dispatcher.add_handler(CommandHandler("message", message))
    dispatcher.add_handler(CommandHandler("orders", orders))
    dispatcher.add_handler(CommandHandler("setstatus", setstatus))
    dispatcher.add_handler(CommandHandler("ubalance", ubalance))

    # Utils
    dispatcher.add_handler(MessageHandler(Filters.text, all_messages))
    dispatcher.add_handler(MessageHandler(Filters.photo | Filters.document, get_docs))

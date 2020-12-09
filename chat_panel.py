import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputMediaPhoto, \
    InputMediaDocument, ChatPermissions

from menu import Menu
from models import *
from core import *
from menu import *

CHANNEL_ID = '-1001361464885'
MEDIA_ID = '-1001412307468'


@db_session
def chat(update, context):
    if update.message.chat.id < 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'admin':
                text = 'Используйте /chat order_id'
                if context.args:
                    order = Order.get(id=int(context.args[0]))
                    chat = Chat.get(chat_id=update.effective_chat.id)
                    if order and not chat:
                        # context.bot.set_chat_title(chat_id=update.effective_chat.id, title='None')
                        # context.bot.set_chat_description(chat_id=update.effective_chat.id, description='None')

                        title = "Заказ #" + str(order.id) + ' (' + order.subject + ')'
                        context.bot.set_chat_title(chat_id=update.effective_chat.id, title=title)

                        # description = 'Чат по поводу заказа ' + order.subject + ' [' + str(order.id) + ']'
                        # context.bot.set_chat_description(chat_id=update.effective_chat.id, description=description)

                        chat_permissions = ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_polls=True,
                            can_send_other_messages=True,
                            can_add_web_page_previews=True,
                            can_change_info=False,
                            can_invite_users=False,
                            can_pin_messages=False
                        )
                        context.bot.set_chat_permissions(chat_id=update.effective_chat.id, permissions=chat_permissions)

                        # ftext = 'Установленно имя чата - ' + title + '\nУстановленно опсиание чата - ' + description
                        # context.bot.send_message(chat_id=update.effective_chat.id, text=ftext, timeout=500)

                        link = context.bot.export_chat_invite_link(chat_id=update.effective_chat.id)

                        client = User.get(id=int(order.user_id))
                        text = 'Чат с исполнителем по поводу заказа #{} ({}): {}'.format(order.id, order.subject, link)
                        context.bot.send_message(chat_id=client.user_id, text=text, parse_mode=telegram.ParseMode.HTML,)

                        worker = User.get(id=int(order.worker_id))
                        text = 'Чат с клиентом по поводу заказа #{} ({}): {}'.format(order.id, order.subject, link)
                        context.bot.send_message(chat_id=worker.user_id, text=text, parse_mode=telegram.ParseMode.HTML,)

                        mymenu = Menu()
                        reply_markup = mymenu.get_menu(tag='#chat#0')

                        pintext = 'Команды чата 👇\n/price <i>цена</i> - утвердить цену\n/admin - вызвать менеджера\n/done - завершить заказ'
                        pinid = context.bot.send_message(chat_id=update.effective_chat.id, text=pintext, timeout=500, reply_markup=reply_markup[0], parse_mode=telegram.ParseMode.HTML,)
                        context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=pinid.message_id)

                        chat = Chat(chat_id=update.effective_chat.id, price='0', user_id=str(order.user_id), worker_id=str(order.worker_id), order_id=str(order.id))
                        # text = 'Чат успешно создан'
                        # context.bot.send_message(chat_id=update.effective_chat.id, text=text, timeout=500)

                    else:
                        text = 'Заказ #' + context.args[0] + ' не найден или чат уже создан.'
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text, timeout=500, parse_mode=telegram.ParseMode.HTML,)


@db_session
def admin(update, context):
    if update.message.chat.id < 0:
        user = get_user(update.message.from_user.id)
        if user:
            chat = Chat.get(chat_id=update.effective_chat.id)
            if chat:
                order = Order.get(id=int(chat.order_id))
                link = context.bot.export_chat_invite_link(chat_id=update.effective_chat.id)
                text = 'Чат ' + str(chat.id) + ' вызывает админа по поводу заказа ' + order.subject + ' [' + str(order.id) + ']'
                text += '\n' + link

                admins = list(select(u for u in User if u.status == 'admin'))

                for a in admins:
                    context.bot.send_message(chat_id=a.user_id, text=text)


@db_session
def price(update, context):
    if update.message.chat.id < 0:
        user = get_user(update.message.from_user.id)
        if user:
            chat = Chat.get(chat_id=update.effective_chat.id)
            if chat:
                order = Order.get(id=int(chat.order_id))

                if context.args:
                    try:
                        price = int(context.args[0])
                        if chat.price == '0':
                            if user:
                                name = get_name(user)

                            chat.worker_yes = 0
                            chat.user_yes = 0

                            if chat.price_msg:
                                context.bot.delete_message(chat_id=chat.chat_id, message_id=chat.price_msg)

                            text = "Пользователь " + name + ' предлагает цену <b>' + context.args[0] + ' руб.</b>\nНажмите на кнопку ниже, если Вы согласны 👇'
                            text += '\nСогласны:\n'

                            mymenu = Menu()
                            buttons = [InlineKeyboardButton('Согласен', callback_data='@' + str(chat.id) + '@yes@' + context.args[0])]

                            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                            reply_markup = InlineKeyboardMarkup(markup)

                            chat.price_msg = context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup).message_id
                        else:
                            text = 'Цена для этого заказа уже утверждена!'
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,)
                    except Exception as e:
                        print(e)
                        text = 'Используйте /price <i>цена</i>, где <i>цена</i> - целое число.'
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,)
                else:
                    text = 'Используйте /price <i>цена</i>, где <i>цена</i> - целое число.'
                    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,)


@db_session
def done(update, context):
    if update.message.chat.id < 0:
        user = get_user(update.message.from_user.id)
        if user:
            chat = Chat.get(chat_id=update.effective_chat.id)
            if chat:
                order = Order.get(id=int(chat.order_id))
                name = get_name(user)

                if order.status == 'Оплачен':
                    print(1)
                    if chat.worker_yes != 2 or chat.user_yes != 2:
                        chat.worker_yes = 1
                        chat.user_yes = 1

                        if chat.done_msg:
                            context.bot.delete_message(chat_id=chat.chat_id, message_id=chat.done_msg)

                        text = "Пользователь " + name + ' предлагает завершить заказ.\nНажмите на кнопку ниже, если Вы согласны 👇'
                        text += '\nСогласны:\n'

                        mymenu = Menu()
                        buttons = [InlineKeyboardButton('Согласен', callback_data='@' + str(chat.id) + '@done')]

                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                        reply_markup = InlineKeyboardMarkup(markup)

                        chat.done_msg = context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,
                                                 reply_markup=reply_markup).message_id
                    else:
                        text = 'Этот заказ уже закрыт!'
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                else:
                    text = 'Этот заказ ещё не оплачен!'
                    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

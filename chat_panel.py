import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputMediaPhoto, \
    InputMediaDocument, ChatPermissions
from telegram.ext import Handler

from menu import Menu
from models import *
from core import *
from menu import *


@db_session
def create_chat(update, context):
    print(1)
    if update.message.chat.id < 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'admin':
                text = 'Используйте /create_chat order_id'
                if context.args:
                    order = Order.get(id=int(context.args[0]))
                    chat = Chat.get(chat_id=update.effective_chat.id)
                    print(order, chat)
                    if order and not chat:
                        title = "Заказ #" + str(order.id) + ' (' + order.subject + ')'
                        context.bot.set_chat_title(chat_id=update.effective_chat.id, title=title)

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

                        link = context.bot.export_chat_invite_link(chat_id=update.effective_chat.id)

                        client = User.get(id=int(order.user_id))
                        text = 'Чат с исполнителем по заказу #{} ({}) успешно создан 👉 {}'.format(order.id, order.subject, link)
                        context.bot.send_message(chat_id=client.user_id, text=text, parse_mode=telegram.ParseMode.HTML,)

                        worker = User.get(id=int(order.worker_id))
                        text = 'Чат с клиентом по заказу #{} ({}) успешно создан 👉 {}'.format(order.id, order.subject, link)
                        context.bot.send_message(chat_id=worker.user_id, text=text, parse_mode=telegram.ParseMode.HTML,)

                        order_text = get_order(id=order.id) +\
                                     f"\nКлиент: {get_name(client, id=True)}\nИсполнитель: {get_name(worker, id=True)}"
                        context.bot.send_message(chat_id=update.effective_chat.id, text=order_text,
                                                 parse_mode=telegram.ParseMode.HTML,)

                        context.bot.send_message(chat_id=update.effective_chat.id,
                                                 text='Ожидайте всех участников сделки.',)

                        chat = Chat(chat_id=update.effective_chat.id, price='0', user_id=str(order.user_id),
                                    worker_id=str(order.worker_id), order_id=str(order.id), chat_link=link,
                                    status='wait')
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

                            text = name + ' предлагает цену - <b>' + context.args[0] + ' руб.</b>\n' \
                                'Если вы согласны, нажмите на кнопку "Согласен"👇 Действие требуется от обеих сторон!\n'
                            # text += '\nСогласны:\n'

                            mymenu = Menu()
                            buttons = [InlineKeyboardButton('Согласен', callback_data='@' + str(chat.id) + '@yes@' + context.args[0])]

                            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                            reply_markup = InlineKeyboardMarkup(markup)

                            chat.price_msg = context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                                                      parse_mode=telegram.ParseMode.HTML,
                                                                      reply_markup=reply_markup).message_id
                        else:
                            text = 'Цена для этого заказа уже утверждена!'
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,)
                    except Exception as e:
                        print(e)
                        text = 'Напишите "/price [<b>цена</b>]", где [<b>цена</b>] - целое число.'
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,)
                else:
                    text = 'Напишите "/price [<b>цена</b>]", где [<b>цена</b>] - целое число.'
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

                        username = get_name(User.get(id=int(chat.user_id)))

                        text = f'{name} предлагает завершить заказ.\nЕсли вы согласны, нажмите на кнопку "Согласен"👇' \
                            f' Действие требуется от обеих сторон!\n\n⚠️ {username}, нажимая на кнопку "Согласен"' \
                            f' Вы подтверждаете, что убедились в корректности предоставленной работы, и не ' \
                            f'имеете претензий к исполнителю и сервису StudyX.\n'
                        # text += '\nСогласны:\n'

                        mymenu = Menu()
                        buttons = [InlineKeyboardButton('Согласен', callback_data='@' + str(chat.id) + '@done')]

                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                        reply_markup = InlineKeyboardMarkup(markup)

                        chat.done_msg = context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML,
                                                 reply_markup=reply_markup).message_id
                    else:
                        text = 'Этот заказ завершён!'
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                else:
                    text = 'Этот заказ ещё не оплачен!'
                    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

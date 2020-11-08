import time

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from menu import Menu
from models import *
from core import *
from menu import *
from transaction import Transaction
from user_panel import *

tr = Transaction


@db_session
def adminpanel(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        mymenu = Menu()
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if len(context.args) > 0:
                password = Settings.get(key='password').value
                if context.args[0] == password:
                    user.status = 'admin'
                    reply_markup = mymenu.get_menu(tag='#admin#0')
                    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_markup[1], reply_markup=reply_markup[0])
            else:
                user.status = 'user'
                reply_markup = mymenu.get_menu(tag='#main#0')
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply_markup[1],
                                         reply_markup=reply_markup[0])
        else:
            start(update, context)


def channel(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                if context.args:
                    context.bot.send_message(chat_id=CHANNEL_ID, text=' '.join(context.args))
                else:
                    context.bot.send_message(chat_id=CHANNEL_ID, text='Hello World!')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def message(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                text = 'Используйте /message user_id text'
                chat_id = update.effective_chat.id
                if context.args:
                    if len(context.args) >= 2:
                        user = User.get(id=int(context.args[0]))
                        if user:
                            text = ' '.join(context.args[1:])
                            chat_id = user.id
                        else:
                            text = 'Пользователь с id ' + context.args[0] + ' не найден'
                context.bot.send_message(chat_id=chat_id, text=text)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def ubalance(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                text = 'Используйте /ubalance user_id [-/+]amount'
                chat_id = update.effective_chat.id
                if context.args:
                    if len(context.args) >= 2:
                        user = User.get(id=int(context.args[0]))
                        if user:
                            amount = int(' '.join(context.args[1:]))
                            chat_id = user.id
                            user.balance += amount
                            t = tr.new(type='ADMINREBALANCE', bill_id='None', amount=int(amount), user_id=user.id,
                                       date=time.strftime('%d.%M.%Y'))
                            text = 'Баланс пользователя ' + get_name(user) + ' изменен на ' + str(amount) + 'р.'
                        else:
                            text = 'Пользователь с id ' + context.args[0] + ' не найден'
                context.bot.send_message(chat_id=chat_id, text=text)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


def user(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                try:
                    id = int(context.args[0])
                    find_user = get_user(id)
                    if find_user:
                        mymenu = Menu()
                        buttons = [InlineKeyboardButton('Заказы', callback_data='@' + str(id) + '@userorders'),
                                   InlineKeyboardButton('Баланс', callback_data='@' + str(id) + '@userbalance'),
                                   InlineKeyboardButton('Сделать исполнителем', callback_data='@' + str(id) + '@makeworker'),
                                   InlineKeyboardButton('Забанить', callback_data='@' + str(id) + '@ban'),
                                   ]

                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                        reply_markup = InlineKeyboardMarkup(markup)
                        text = get_profile(find_user.id)
                    else:
                        reply_markup = None
                        text = 'Пользователь с id ' + str(id) + ' не найден'
                except Exception as e:
                    text = 'Используйте /user user_id'
            else:
                text = 'Вы не являетесь админом'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
        else:
            start(update, context)


@db_session
def getorder(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                reply_markup = InlineKeyboardMarkup([])
                if context.args:
                    try:
                        id = int(context.args[0])
                        order = Order.get(id=id)
                        u = User.get(id=int(order.user_id))
                        text = '<b>' + get_name(u) + '[' + str(u.id) + ']</b>\n'
                        text += get_order(id)
                        order = Order.get(id=id)

                        mymenu = Menu()
                        buttons = [InlineKeyboardButton('Одобрить', callback_data='@' + str(id) + '@push'),
                                    InlineKeyboardButton('Удалить', callback_data='@' + str(id) + '@del')]

                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                        reply_markup = InlineKeyboardMarkup(markup)
                    except Exception as e:
                        print(e)
                        text = 'Используйте /getorder Номер_заказа!'
                else:
                    text = 'Используйте /getorder Номер_заказа!'

                if order.docs:
                    text += '\nВложения:\n' + order.docs

                context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


@db_session
def orders(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            markup = ''
            if user.status == 'admin':
                try:
                    orders = select(o for o in Order)
                    text = 'Заказы:\n'
                    buttons = []
                    for order in list(orders):
                        text += '#' + str(order.id) + ' - ' + order.subject + ' [' + str(order.status) + ']['\
                                +str(order.user_id)+']\n'
                        buttons.append(InlineKeyboardButton('Заказ ' + str(order.id), callback_data="@" + str(order.id)))
                    mymenu = Menu()
                    markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                except Exception as e:
                    print(e)
                    text = 'Заказы не найденны'
            else:
                text = 'Вы не являетесь админом'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(markup))
        else:
            start(update, context)


@db_session
def setstatus(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                text = 'Используйте /setstatus user_id status'
                if context.args:
                    if len(context.args) >= 2:
                        user = User.get(id=int(context.args[0]))
                        if user:
                            user.status = context.args[1]
                            text = 'Вы успешно изменили статус пользователя с id ' + str(user.id) + ' на ' + context.args[1]
                            context.bot.send_message(chat_id=user.id, text='Ваш статус изменен на ' + context.args[1])
                        else:
                            text = 'Пользователь с id ' + context.args[0] + ' не найден'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)

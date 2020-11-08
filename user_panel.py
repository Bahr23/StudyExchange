import datetime

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputMediaPhoto, \
    InputMediaDocument

from menu import Menu
from models import *
from core import *
from menu import *

@db_session
def start(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        mymenu = Menu()
        reply_markup = mymenu.get_menu(tag='#main#0')
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            text = "Добро пожаловать <b>" + user.first_name + '</b>'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0], parse_mode=telegram.ParseMode.HTML)
        else:
            user = update.message.from_user
            first_name = user.first_name if user.first_name else 'Не указано'
            last_name = user.last_name if user.last_name else 'Не указано'
            username = user.username if user.username else str(user.id)
            age = 'Не указано'
            education = 'Не указано'
            city = 'Не указано'
            registration_date = str(datetime.date.today()).replace('-', '.')
            last_order = 'Не указано'
            orders_number = '0'
            workers_orders = 0
            rate = 0
            points = 0
            balance = 0

            newuser = User(id=user.id, status='user', first_name=first_name, last_name=last_name,
                           username=username, age=age, education=education, city=city, registration_date=registration_date,
                           last_order=last_order, orders_number=orders_number, workers_orders=workers_orders,
                           rate=rate, points=points, balance=balance)
            context.user_data.update({'queue': False})
            text = newuser.first_name + ", вы успешно зарегистрировались!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0])


def all_messages(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:

                    ans = None

                    if context.user_data['queue_docs'] != '':
                        ans = context.user_data['queue_docs']
                        context.user_data['queue_docs'] = ''

                    if context.user_data['queue_name'] != 'edit_order':
                        current_queue(update, context, user)

                    queue(update, context, user, ans)
                    return
            context.user_data.update({'last_message': update.message.text})
            mymenu = Menu()
            reply_markup = mymenu.get_menu(tag='#main#0')
            text = user.first_name + ', я не знаю как на это ответить'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0])
        else:
            start(update, context)


def get_docs(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    if list(context.user_data['queue_list'][context.user_data['queue_position']].keys())[0] == 'docs':
                        if update.message.photo:
                            text = "Фото сохранено, отправьте еще или нажмите 'Готово'"
                            fid = update.message.photo[0].file_id

                            context.user_data['queue_docs'] += fid + ', '


                            # context.bot.send_photo(chat_id=MEDIA_ID, photo=update.message.photo[0].file_id)
                        if update.message.document:
                            text = 'Отправьте медиа как фото, а не файлы'
                            # context.bot.send_document(chat_id=MEDIA_ID, document=update.message.document.file_id)

                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                    else:
                        queue(update, context, user)
                        return
            else:
                mymenu = Menu()
                reply_markup = mymenu.get_menu(tag='#main#0')
                text = user.first_name + ', я не знаю как на это ответить'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0])
                context.user_data.update({'last_message': update.message.text})

        else:
            start(update, context)


def stop(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
        context.bot.send_message(chat_id=update.effective_chat.id, text='Вы закончили очередь.')


@db_session
def profile(update, context):
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
            text = 'Используйте /profile id_пользователя'
            if context.args:
                user = User.get(id=int(context.args[0]))
                if user:
                    text = get_profile(user.id)
                else:
                    text = 'Пользователь с id ' + context.args[0] + ' не найден'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


def myprofile(update, context):
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
            text = get_profile(user.id)

            mymenu = Menu()
            buttons = [InlineKeyboardButton('Редактировать', callback_data='@' + str(user.id) + '@profile@list'),
                       InlineKeyboardButton('Хочу стать исполнителем', callback_data='@' + str(user.id) + '@want')]

            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
            reply_markup = InlineKeyboardMarkup(markup)

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
        else:
            start(update, context)


def menu(update, context):
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
            mymenu = Menu()
            reply_markup = mymenu.get_menu(tag='#main#0')
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_markup[1], reply_markup=reply_markup[0])
        else:
            start(update, context)
    else:
        mymenu = Menu()
        reply_markup = mymenu.get_menu(tag='#chat#0')
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_markup[1], reply_markup=reply_markup[0])


def new_order(update, context):
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
            queue_list = [
                {'subject': 'Выберите предмет (или напишите свой):', 'menu': "#subject#0"},
                {'type': 'Выберите тип работы (или напишите свой):', 'menu': '#type#0'},
                {'faculty': 'Укажите ваш факультет? (не обязательно)', 'menu': '#faculty#0'},
                {'departament': 'Укажите вашу кафедру? (не обязательно)', 'menu': '#departament#0'},
                {'teacher': 'Укажите вашего преподователя? (не обязательно)', 'menu': '#teacher#0'},
                {'description': 'Укажите описание работы:', 'menu': None},
                {'deadline': 'Выберите срок (или укажите свой срок):', 'menu': '#deadline#0'},
                {'price': 'Выберите цену (или укажите свою цену):', 'menu': '#price#0'},
                {'docs': 'Прикрепите фотографии и нажмите кнопку "Готово"', 'menu': '#done#0'},
            ]
            context.user_data.update({'queue': True, 'queue_name': 'new_order', 'queue_finish': 'Вы успешно создали заказ!',
                                      'queue_list': queue_list, 'queue_position': 0, 'queue_answers': [], 'queue_docs': '',
                                      'last_queue_message': ''})

            current_queue(update, context, user)
        else:
            start(update, context)


@db_session
def my_orders(update, context):
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
            orders = select(o for o in Order if o.user_id == user.id)
            text = 'Ваши заказы:\n'
            buttons = []
            for order in list(orders):
                text += '#' + str(order.id) + ' - ' + order.subject + ' [' + order.status + ']\n'
                buttons.append(InlineKeyboardButton('Заказ ' + str(order.id), callback_data="@" + str(order.id)))

            mymenu = Menu()
            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(markup))
        else:
            start(update, context)


@db_session
def del_order(update, context):
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

            if context.args:
                try:
                    id = int(context.args[0])
                    text = delete_order(id)
                except Exception as e:
                    text = 'Используйте /delorder Номер_заказа!'
            else:
                text = 'Используйте /delorder Номер_заказа!'

            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        else:
            start(update, context)


@db_session
def order(update, context):
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
            reply_markup = InlineKeyboardMarkup([])
            if context.args:
                try:
                    id = int(context.args[0])
                    order = Order.get(id=id)
                    text = get_order(id)

                    if order.user_id != user.id and user.status != 'admin':
                        text = False
                    if not text:
                        text = 'Заказ №' + str(id) + ' не найден!'
                    else:
                        workers = order.worker_id
                        mymenu = Menu()
                        reply_markup = mymenu.order_buttons(id, workers)
                except Exception as e:
                    text = 'Используйте /order Номер_заказа!'
            else:
                text = 'Используйте /order Номер_заказа!'

            if order.docs:
                text += '\nВложения:\n' + order.docs

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


def balance(update, context):
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
            text = 'Ваш баланс - ' + str(user.balance) + 'р'

            mymenu = Menu()
            buttons = [InlineKeyboardButton('Пополнить', callback_data='@' + str(user.id) + '@deposit'),
                       InlineKeyboardButton('Вывести', callback_data='@' + str(user.id) + '@withdraw'),
                       InlineKeyboardButton('История', callback_data='@' + str(user.id) + '@balancehistory')]

            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
            reply_markup = InlineKeyboardMarkup(markup)

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        else:
            start(update, context)

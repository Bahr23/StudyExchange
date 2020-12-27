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
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT, parse_mode=telegram.ParseMode.HTML)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            text = 'Рад снова Вас видеть, ' + user.first_name + '! По всем вопросам пишите Вашему <a href="https://t.me/alexmustdie">персональному менеджеру</a> 👨‍💻'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0], parse_mode=telegram.ParseMode.HTML)
        else:
            user = update.message.from_user
            first_name = user.first_name if user.first_name else 'не указано'
            last_name = user.last_name if user.last_name else 'не указано'
            username = user.username if user.username else str(user.id)
            age = 'не указано'
            education = 'не указано'
            city = 'не указано'
            registration_date = str(datetime.date.today()).replace('-', '.')
            last_order = 'не указано'
            orders_number = '0'
            workers_orders = 0
            rate = 0
            points = 0
            balance = 0

            newuser = User(user_id=user.id, status='user', first_name=first_name, last_name=last_name,
                           username=username, age=age, education=education, city=city, registration_date=registration_date,
                           last_order=last_order, orders_number=orders_number, workers_orders=workers_orders,
                           rate=rate, points=points, balance=balance)
            context.user_data.update({'queue': False})
            text = 'Вы успешно зарегистрировались на StudyX! По всем вопросам пишите Вашему <a href="https://t.me/alexmustdie">персональному менеджеру</a> 👨‍💻'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0], parse_mode=telegram.ParseMode.HTML)


def all_messages(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
            text = user.first_name + ', я не знаю как на это ответить 😔'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0])
        else:
            start(update, context)


def get_docs(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    if list(context.user_data['queue_list'][context.user_data['queue_position']].keys())[0] == 'docs':
                        if update.message.photo:
                            text = 'Фото сохранено, отправьте ещё или нажмите "Готово" 👇'
                            fid = update.message.photo[0].file_id

                            context.user_data['queue_docs'] += fid + ', '


                            # context.bot.send_photo(chat_id=MEDIA_ID, photo=update.message.photo[0].file_id)
                        if update.message.document:
                            text = 'Отправьте вложение, как фото, а не файлы!'
                            # context.bot.send_document(chat_id=MEDIA_ID, document=update.message.document.file_id)

                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                    else:
                        queue(update, context, user)
                        return
            else:
                mymenu = Menu()
                reply_markup = mymenu.get_menu(tag='#main#0')
                text = user.first_name + ', я не знаю как на это ответить 😔'
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
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            text = 'Используйте /profile <i>id_пользователя</i>'
            if context.args:
                user = User.get(id=int(context.args[0]))
                if user:
                    text = get_profile(user.id)
                else:
                    text = 'Такой пользователь не найден 😔'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


def myprofile(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            text = get_profile(user.id)

            mymenu = Menu()
            buttons = [InlineKeyboardButton('Редактировать', callback_data='@' + str(user.id) + '@profile@list')]

            if not user.wanted:
                buttons.append(InlineKeyboardButton('Хочу стать исполнителем 👋', callback_data='@' + str(user.id) + '@want'))

            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
            reply_markup = InlineKeyboardMarkup(markup)

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
        else:
            start(update, context)


def menu(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            mymenu = Menu()
            reply_markup = mymenu.get_menu(tag='#main#0')
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_markup[1], reply_markup=reply_markup[0], parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)
    else:
        mymenu = Menu()
        reply_markup = mymenu.get_menu(tag='#chat#0')
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_markup[1], reply_markup=reply_markup[0])


def new_order(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            queue_list = [
                {'subject': 'Выберите предмет из списка или укажите его в ответном сообщении 👇', 'menu': "#subject#0"},
                {'type': 'Выберите тип работы из списка или укажите его в ответном сообщении 👇', 'menu': '#type#0'},
                {'description': 'Укажите описание работы 👇', 'menu': None},
                {'deadline': 'Выберите срок выполнения работы из списка или укажите его в ответном сообщении 👇\n'
                             '\np.s. Если требуется помощь в онлайн-режиме, '
                             'то укажите дату и время проведения работы (по Москве).', 'menu': '#deadline#0'},
                {'price': 'Выберите желаемый ценовой диапазон из списка или укажите свою цену в ответном сообщении 👇', 'menu': '#price#0'},
                {'faculty': 'Укажите Ваш факультет 👇', 'menu': '#faculty#0'},
                {'departament': 'Укажите Вашу кафедру 👇', 'menu': '#departament#0'},
                {'teacher': 'Укажите ФИО преподавателя 👇', 'menu': '#teacher#0'},
                {'docs': 'Прикрепите фотографии, если это необходимо, и нажмите "Готово" 👇', 'menu': '#done#0'},
                {'promo': 'Укажите промокод, если он у Вас есть, или нажмите "Отправить" 👇', 'menu': '#promo#0'},
            ]
            context.user_data.update({
                'queue': True,
                'queue_name': 'new_order',
                'queue_finish': 'Заказ успешно создан и отправлен на проверку.'
                                ' Вам придёт уведомление, когда он будет одобрен 👌',
                'queue_list': queue_list,
                'queue_position': 0,
                'queue_answers': [],
                'queue_docs': '',
                'last_queue_message': ''})

            current_queue(update, context, user)
        else:
            start(update, context)


@db_session
def my_orders(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            orders = select(o for o in Order if o.user_id == user.id)
            if len(orders):
                text = '' # Ваши заказы:\n
                buttons = []
                for order in list(orders):
                    text += '#' + str(order.id) + ' - ' + order.subject + ' (' + order.status + ')\n'
                    buttons.append(InlineKeyboardButton('Заказ #' + str(order.id), callback_data="@" + str(order.id)))

                mymenu = Menu()
                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(markup))
            else:
                text = 'У Вас пока нет ни одного заказа 😔'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        else:
            start(update, context)


@db_session
def del_order(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
                    text = 'Используйте /delorder <i>id_заказа</i>!'
            else:
                text = 'Используйте /delorder <i>id_заказа</i>!'

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


@db_session
def order(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
                        text = 'Заказ #' + str(id) + ' не найден 😔'
                    else:
                        workers = order.worker_id
                        mymenu = Menu()
                        reply_markup = mymenu.order_buttons(id, workers)
                        if order:
                            if order.docs != 'Вложения не добавлены':
                                text += '\nВложения:\n' + order.docs
                except Exception as e:
                    text = 'Используйте /order <i>id_заказа</i>!'
            else:
                text = 'Используйте /order <i>id_заказа</i>!'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


def balance(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            text = 'Ваш баланс: ' + str(user.balance) + ' руб.'

            mymenu = Menu()
            buttons = [InlineKeyboardButton('Пополнить', callback_data='@' + str(user.id) + '@deposit'),
                       InlineKeyboardButton('Вывести', callback_data='@' + str(user.id) + '@withdraw'),
                       InlineKeyboardButton('История', callback_data='@' + str(user.id) + '@balancehistory')]

            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
            reply_markup = InlineKeyboardMarkup(markup)

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        else:
            start(update, context)


def faq(update, context):
    if update.message.chat.id > 0:
        context.user_data.update({'queue': False})
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return

            text = "1. Вы оформляете новый заказ на выполнение студенческой работы через этого бота (/neworder)." \
                   "\n2. Ваша заявка отправляется на рассмотрение менеджеру и спустя время публикуется " \
                   "<a href='https://t.me/StudyExchangePosts/'>на канале</a> с заказами." \
                   "\n3. Исполнители отправляют заявки на выполнение Вашего заказа, о чём Вы получаете уведомления " \
                   "в боте." \
                   "\n4. После того, как Вы выберете подходящего исполнителя, менеджер создаст общий чат, где Вы " \
                   " должны договориться со специалистом об условиях работы." \
                   "\n5. Далее Вам необходимо внести оплату в полном размере. Эти средства будут удержаны на счёте администрации " \
                   "биржи, исполнитель не получит к ним доступ до завершения заказа." \
                   "\n6. Когда работа готова, Вы проверяете её и подтверждаете соблюдение оговорённых условий. " \
                   "Теперь исполнитель получит оплату, а Вы сможете оценить его работу." \
                   '\n\nПо всем вопросам пишите Вашему <a href="https://t.me/alexmustdie">персональному менеджеру</a>.'

            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)

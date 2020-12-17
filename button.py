import datetime
import json
import time

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputMediaPhoto

from menu import Menu
from models import *
from core import *
from menu import *
from transaction import Transaction

tr = Transaction


@db_session
def button(update, context):
    query = update.callback_query
    mymenu = Menu()
    user = get_user(update.callback_query.from_user.id)
    if user:
        if user.status == 'banned':
            context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
            return
    transction = Transaction
    if query.message.chat.id != int(CHANNEL_ID):
        if query.data[0] == '#':
            mymenu = Menu()
            reply_markup = mymenu.get_menu(tag=query.data)
            query.edit_message_text(text=reply_markup[1], reply_markup=reply_markup[0])
        else:
            user = get_user(update.callback_query.from_user.id)
            if user:
                if 'queue' in context.user_data.keys():
                    if context.user_data['queue']:
                        queue(update, context, user)
                        return

                if query.data[0] == '@':
                    args = query.data.split('@')
                    if len(args) == 2:
                        try:
                            id = int(query.data[1:])
                            order = Order.get(id=id)
                            text = get_order(id)
                            mymenu = Menu()
                            reply_markup = mymenu.order_buttons(id)
                        except Exception as e:
                            print(e)
                            text = 'Используйте /order id_заказа!'

                        # if order:
                        #     if order.docs != 'Вложения не добавлены.':
                        #         text += '\nВложения:\n' + order.docs

                        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
                    else:
                        if args[2] == 'ban':
                            text = 'Используйте <b>/setstatus user_id banned</b> для блокировки пользователя\n' \
                                   'Используйте <b>/setstatus user_id user</b> для разблокировки пользователя'
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'makeworker':
                            user = User.get(id=int(args[1]))
                            if user:
                                user.status = 'worker'
                                text = 'Вы успешно изменили статус пользователя' + get_name(user) + '[' + str(user.id) + '] на worker'
                                context.bot.send_message(chat_id=user.user_id, text='Ваша заявка на роль исполнителя только что была одобрена. Можете приступать к работе!')
                            else:
                                text = 'Такой пользователь не найден.'
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'userbalance':
                            user = User.get(id=int(args[1]))
                            if user:
                                text = '<b>' + get_name(user) + '[' + str(user.id) + ']</b>\n'
                                text += '<i>Текущий баланс</i> - ' + str(user.balance) + 'р\n\n'

                                transctions = list(select(t for t in Transactions if t.user_id == user.id))

                                text += '<i>История транзакций</i>:\n'
                                if transctions:
                                    for t in transctions[0:19]:
                                        text += transction.get(t.id) + '\n'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'userorders':
                            user = User.get(id=int(args[1]))
                            if user:
                                text = '<b>Незавершенные заказы пользователя ' + get_name(user) + '[' + str(user.id) + ']</b>\n' \
                                        '<i>Используйте /getorder для получения полной инофрмации</i>\n\n'

                                orders = list(select(o for o in Order if o.user_id == user.id and o.status != 'Завершён'))

                                if orders:
                                    for o in orders:
                                        text += o.subject + '[' + str(o.id) + '] | ' + o.status + ' | ' + str(o.price) + '\n'\

                                buttons = [InlineKeyboardButton('Заверешенные заказы', callback_data='@' + str(user.id) + '@userfinishedorders'),]

                                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                                           footer_buttons=None)
                                reply_markup = InlineKeyboardMarkup(markup)

                                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                                         parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)

                        if args[2] == 'userfinishedorders':
                            user = User.get(id=int(args[1]))
                            if user:
                                text = '<b>Завершённые заказы пользователя ' + get_name(user) + '[' + str(user.id) + ']</b>\n' \
                                        '<i>Используйте /getorder для получения полной инофрмации</i>\n\n'

                                orders = list(select(o for o in Order if o.user_id == user.id and o.status == 'Завершён'))

                                if orders:
                                    for o in orders:
                                        text += o.subject + '[' + str(o.id) + '] | ' + o.status + ' | ' + str(o.price) + '\n'\


                                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                                         parse_mode=telegram.ParseMode.HTML)


                        if args[2] == 'workers':
                            myorder = Order.get(id=int(args[1]))
                            workers = myorder.worker_id.split(',')[:-1]

                            if workers:
                                text = '' # 'Текущие исполнители для заказа #' + args[1] + ':\n'
                                buttons = []

                                for w in workers:
                                    wor = User.get(id=int(w))
                                    label = wor.first_name + ' ' + ' (' + str(wor.id) + ')\n'
                                    text += label
                                    buttons.append(InlineKeyboardButton('Выбрать ' + label, callback_data='@' + args[1] + '@choose@' + str(wor.id)))

                                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                                reply_markup = InlineKeyboardMarkup(markup)
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
                            else:
                                text = 'Пока никто не отправил заявку на выполнение этого заказа.'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'want':
                            if not user.wanted:
                                user = User.get(id=int(args[1]))

                                text = 'Пользователь ' + get_name(user, True) + ' хочет стать исполнителем!'

                                name = get_name(user)

                                label = name + ' (id' + str(user.id) + ')\n'
                                buttons = [InlineKeyboardButton('Профиль ' + label,
                                                                callback_data='@' + str(user.id) + '@showprofile'),
                                           ]
                                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                                           footer_buttons=None)

                                reply_markup = InlineKeyboardMarkup(markup)

                                admins = list(select(u for u in User if u.status == 'admin'))
                                for admin in admins:
                                    context.bot.send_message(chat_id=admin.user_id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)

                                text = 'Вы успешно отправили заявку на роль исполнителя. Менеджер рассмотрит её в ближайшее время.'
                                user.wanted = True
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
                            else:
                                text = 'Вы уже отправили заявку на роль испольнителя. Ожидайте решение мененджера.'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                                         parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'predel':
                            order = Order.get(id=int(args[1]))
                            if order.status != 'Оплачен':
                                text = 'Вы уверены, что хотите удалить заказ #{} ({})?'.format(order.id, order.subject)
                                buttons = [
                                    InlineKeyboardButton('Да', callback_data='@' + str(order.id) + '@del')]
                                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                                           footer_buttons=None)
                                reply_markup = InlineKeyboardMarkup(markup)
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                                         reply_markup=reply_markup)
                            else:
                                text = 'Заказ невозможно удалить, потому что он уже оплачен. Пожалуйста, свяжитесь с мененджером для решения этой проблемы.'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'del':
                            order = Order.get(id=int(args[1]))
                            if order.status != 'Оплачен':
                                id = int(args[1])

                                if order.worker_id:
                                    for w in order.worker_id.split(','):
                                        if w != '':
                                            wr = User.get(id=int(w))
                                            text = 'К сожалению, по заказу #{} ({}) был выбран другой исполнитель или заказ был отменён.'.format(order.id, order.subject)
                                            context.bot.send_message(chat_id=wr.user_id, text=text,
                                                                     parse_mode=telegram.ParseMode.HTML)

                                chat = Chat.get(order_id=str(order.id))
                                if chat:
                                    text = delete_order(id)
                                    context.bot.send_message(chat_id=chat.chat_id, text=text)
                                else:
                                    text = delete_order(id)
                                    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                            else:
                                text = 'Заказ невозможно удалить, потому что он уже оплачен. Пожалуйста, свяжитесь с мененджером для решения этой проблемы.'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'push':
                            myorder = Order.get(id=int(args[1]))

                            myorder.status = 'Поиск исполнителя'

                            text = get_order(int(args[1]))
                            buttons = [InlineKeyboardButton('Взять заказ', callback_data='@' + str(args[1]) + '@take')]
                            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)

                            if myorder:
                                if myorder.docs != 'Вложения не добавлены':
                                    text += '\nВложения:\n' + myorder.docs


                            usert = User.get(id=int(myorder.user_id))

                            post = context.bot.send_message(chat_id=CHANNEL_ID, text=text, reply_markup=InlineKeyboardMarkup(markup), parse_mode=telegram.ParseMode.HTML)
                            post_link = 'https://t.me/StudyExchangePosts/' + str(post.message_id)

                            myorder.channel_message = post.message_id

                            text = 'Заказ #{} ({}) успешно одобрен!'.format(myorder.id, myorder.subject)
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                            text = 'Ваш заказ #{} ({}) одобрен и <a href="{}">опубликован</a> на канале!'.format(myorder.id, myorder.subject, post_link)
                            context.bot.send_message(chat_id=usert.user_id, text=text, parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'buy':
                            order = Order.get(id=int(args[1]))
                            chat = Chat.get(order_id=str(order.id))
                            text = 'Error'
                            if chat:
                                if chat.price != '0' and order.status == 'Ожидает оплаты':
                                    if order.promo != '0':
                                        promo = 1 - float(Coupons.get(name=order.promo).amount) / 100
                                        price = int(int(chat.price) * promo)
                                    else:
                                        price = chat.price

                                    text = 'Вы уверены, что хотите оплатить заказ ' + order.subject + \
                                           ' [' + str(order.id) + '] на сумму ' + str(price) + ' руб?'
                                    buttons = [
                                        InlineKeyboardButton('Да', callback_data='@' + str(order.id) + '@buyyes')]
                                    markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                                               footer_buttons=None)
                                    reply_markup = InlineKeyboardMarkup(markup)
                                    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
                                else:
                                    text = 'Вы еще не утвердили цену с исполнителем или заказ уже оплачен.'
                                    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                            else:
                                text = 'Пока никто не согласился на выполнение этого заказа.'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'buyyes':
                            order = Order.get(id=int(args[1]))
                            chat = Chat.get(order_id=args[1])
                            if chat:
                                if chat.price != '0' and order.status == 'Ожидает оплаты':
                                    if int(chat.price) <= user.balance:

                                        if order.promo != '0':
                                            coup = Coupons.get(name=order.promo)
                                            if coup.count > 0:
                                                promo = 1 - float(coup.amount) / 100
                                                coup.count -= 1
                                                price = int(int(chat.price) * promo)
                                            else:
                                                price = chat.price
                                        else:
                                            price = chat.price

                                        user.balance -= int(price)

                                        message = update.callback_query.message
                                        context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                                      message_id=message.message_id,
                                                                      text=message.text + '\n👉 ОПЛАЧЕНО', reply_markup=None,
                                                                      parse_mode=telegram.ParseMode.HTML)

                                        t = tr.new(type='PAYFORORDER', bill_id='None', amount=-int(chat.price), user_id=user.id,
                                                   date=time.strftime('%d.%M.%Y'))
                                        order.status = 'Оплачен'

                                        context.bot.edit_message_text(chat_id=CHANNEL_ID, message_id=order.channel_message,
                                                          text=get_order(order.id), reply_markup=None, parse_mode=telegram.ParseMode.HTML)

                                        name = get_name(user, True)
                                        context.bot.send_message(chat_id=update.effective_chat.id, text='Заказ успешно оплачен!')
                                        text = 'Клиент успешно оплатил заказ #{} ({}). Можете приступать к работе!'.format(order.id, order.subject)

                                        w = User.get(id=int(chat.worker_id))

                                        context.bot.send_message(chat_id=w.user_id, text=text, parse_mode=telegram.ParseMode.HTML)
                                        context.bot.send_message(chat_id=int(chat.chat_id), text=text, parse_mode=telegram.ParseMode.HTML)
                                    else:
                                        text = 'На балансе недостаточно средств: ' + str(user.balance) + ' руб.'
                                        buttons = [
                                            InlineKeyboardButton('Пополнить', callback_data='@' + str(user.id) + '@deposit')]

                                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                                        reply_markup = InlineKeyboardMarkup(markup)

                                        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
                                else:
                                    text = 'Вы ещё не утвердили цену с исполнителем.'
                                    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
                            else:
                                text = 'Вы не выбрали исполнителя для этого заказа.'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'yes':
                            chat = Chat.get(id=int(args[1]))
                            order = Order.get(id=int(chat.order_id))
                            message = update.callback_query.message

                            if str(user.id) == str(chat.user_id):
                                if chat.user_yes == 0:
                                    name = get_name(user)
                                    chat.user_yes = 1
                                    text = "\nКлиент: " + name
                                    reply_markup = message.reply_markup

                            if str(user.id) == str(chat.worker_id):
                                if chat.worker_yes == 0:
                                    name = get_name(user)
                                    chat.worker_yes = 1
                                    text = "\nИсполнитель: " + name
                                    reply_markup = message.reply_markup

                            if chat.user_yes == 1 and chat.worker_yes == 1:
                                chat.price = args[3]
                                order.status = 'Ожидает оплаты'
                                context.bot.edit_message_text(chat_id=CHANNEL_ID, message_id=order.channel_message,
                                                              text=get_order(order.id), reply_markup=None,
                                                              parse_mode=telegram.ParseMode.HTML)
                                text += '\n<b>Цена утверждена!</b>'
                                reply_markup = None
                                user_text = 'Цена по заказу #{} ({}) утверждена. Для оплаты нажмите на кнопку ниже 👇'.format(order.id, order.subject)

                                buttons = [
                                    InlineKeyboardButton('Оплатить', callback_data='@' + str(order.id) + '@buyyes'),
                                ]

                                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                                markup = InlineKeyboardMarkup(markup)

                                u = User.get(id=chat.user_id)
                                context.bot.send_message(chat_id=u.user_id, text=user_text, reply_markup=markup)

                            context.bot.edit_message_text(chat_id=chat.chat_id, message_id=message.message_id,
                                                          text=message.text + text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'done':
                            print(args)
                            chat = Chat.get(id=int(args[1]))
                            order = Order.get(id=int(chat.order_id))
                            message = update.callback_query.message
                            chat_id = chat.chat_id

                            if str(user.id) == str(chat.user_id):
                                if chat.user_yes == 1:
                                    name = get_name(user)
                                    chat.user_yes = 2
                                    text = "\nКлиент: " + name
                                    reply_markup = message.reply_markup

                            if str(user.id) == str(chat.worker_id):
                                if chat.worker_yes == 1:
                                    name = get_name(user)
                                    chat.worker_yes = 2
                                    text = "\nИсполнитель: " + name
                                    reply_markup = message.reply_markup

                            if chat.user_yes == 2 and chat.worker_yes == 2:
                                u = User.get(id=int(chat.user_id))
                                w = User.get(id=int(chat.worker_id))

                                if u:
                                    u.orders_number = str(int(u.orders_number) + 1)
                                    u.last_order = str(datetime.date.today()).replace('-', '.')
                                if w:
                                    w.orders_number = str(int(w.orders_number) + 1)
                                    u.last_order = str(datetime.date.today()).replace('-', '.')
                                    w.workers_orders += 1

                                    rebalance = int(int(chat.price) * 0.85)

                                    w.balance += rebalance

                                    t = tr.new(type='ORDER', bill_id='None', amount=int(rebalance),
                                               user_id=w.id,
                                               date=str(datetime.datetime.now())[0:19])

                                    wtext = 'Заказ #{} ({}) успешно завершён!'.format(order.id, order.subject)
                                    context.bot.send_message(chat_id=int(w.user_id), text=wtext)

                                    buttons = [
                                        InlineKeyboardButton('⭐', callback_data='@' + str(w.id) + '@rate@1'),
                                        InlineKeyboardButton('⭐⭐', callback_data='@' + str(w.id) + '@rate@2'),
                                        InlineKeyboardButton('⭐⭐⭐', callback_data='@' + str(w.id) + '@rate@3'),
                                        InlineKeyboardButton('⭐⭐⭐⭐', callback_data='@' + str(w.id) + '@rate@4'),
                                        InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data='@' + str(w.id) + '@rate@5'),
                                    ]

                                    markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                                               footer_buttons=None)
                                    reply_markup = InlineKeyboardMarkup(markup)

                                order.status = "Завершён"

                                context.bot.edit_message_text(chat_id=CHANNEL_ID, message_id=order.channel_message,
                                                              text=get_order(order.id), reply_markup=None,
                                                              parse_mode=telegram.ParseMode.HTML)

                                text += '\n<b>Заказ закрыт!</b>'
                                user_text = 'Заказ #{} ({}) успешно завершён!\nПожалуйста, оцените работу иполнителя!'.format(order.id, order.subject)
                                context.bot.send_message(chat_id=int(u.user_id), text=user_text, reply_markup=reply_markup)
                                reply_markup = None
                                chat.delete()

                            context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id,
                                                              text=message.text + text, reply_markup=reply_markup,
                                                              parse_mode=telegram.ParseMode.HTML)


                        if args[2] == 'rate':
                            message = update.callback_query.message
                            context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                          message_id=message.message_id,
                                                          text=message.text,
                                                          parse_mode=telegram.ParseMode.HTML, reply_markup=None)


                            w = User.get(id=int(args[1]))
                            w.points += int(args[3])
                            if w.workers_orders > 0:
                                w.rate = round(w.points / w.workers_orders, 1)
                            else:
                                w.rate = 0

                            text = 'Пользователь ' + get_name(user) + '[' + str(user.id) + '] оценил Вас на ' + args[3] \
                                   + '\nВаш рейтинг: ' + str(w.rate)

                            context.bot.send_message(chat_id=w.user_id, text=text)

                            text = 'Спасибо за оценку исполнителя!\nЖелаем удачи на экзаменах 👌'
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'deposit':
                            user = User.get(id=int(args[1]))

                            queue_list = [
                                {'sum': 'Укажите сумму пополнения 👇', 'menu': None},
                            ]
                            context.user_data.update(
                                {'queue': True, 'queue_name': 'balance', 'queue_finish': None,
                                 'queue_list': queue_list, 'queue_position': 0, 'queue_answers': [], 'queue_docs': '',
                                 'last_queue_message': ''})

                            current_queue(update, context, user)

                        if args[2] == 'withdraw':
                            user = User.get(id=int(args[1]))

                            queue_list = [
                                {'sum': 'Укажите сумму вывода 👇', 'menu': None},
                                {'bank': 'Выберите банк 👇', 'menu': '#banks#0'},
                                {'card': 'Укажите номер Вашей карты 👇', 'menu': None}
                            ]
                            context.user_data.update(
                                {'queue': True, 'queue_name': 'withdraw', 'queue_finish': None,
                                 'queue_list': queue_list, 'queue_position': 0, 'queue_answers': [], 'queue_docs': '',
                                 'last_queue_message': ''})

                            current_queue(update, context, user)

                        if args[2] == 'balancehistory':
                            user = User.get(id=int(args[1]))

                            transctions = list(select(t for t in Transactions if t.user_id == user.id))

                            text = '' # История Ваших транзакций:\n
                            if transctions:
                                for t in transctions[0:19]:
                                    text += transction.get(t.id) + '\n'
                            else:
                                text = 'У Вас пока нет ни одной транзакции.'

                            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        if args[2] == 'showprofile':
                            text = get_profile(int(args[1]))
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

                    if len(args) == 4:
                        if args[2] == 'edit':
                            key = args[3]
                            if key == 'list':
                                reply_markup = mymenu.edit_buttons(args[1])
                                context.bot.send_message(chat_id=update.effective_chat.id, text='Выберите что изменить.', reply_markup=reply_markup)
                            else:
                                if key == 'description':
                                    qmenu = None
                                else:
                                    qmenu = '#' + key + '#0'

                                queue_list = [
                                    {key: 'Укажите Ваши изменения', 'menu': qmenu},
                                ]
                                context.user_data.update(
                                    {'queue': True, 'queue_name': 'edit_order', 'queue_finish': 'Вы изменили заказ!',
                                     'queue_list': queue_list, 'queue_position': 0, 'queue_answers': [],
                                     'edit_order': int(args[1]), 'queue_docs': '', 'last_queue_message': ''})

                                current_queue(update, context, user)

                        if args[2] == 'profile':
                            key = args[3]
                            if key == 'list':
                                reply_markup = mymenu.profile_buttons(args[1])
                                text = 'Что будем редактировать?'
                                context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
                            else:
                                queue_list = [
                                    {key: 'Укажите Ваши изменения 👇', 'menu': None},
                                ]
                                context.user_data.update(
                                    {'queue': True, 'queue_name': 'edit_profile', 'queue_finish': 'Профиль успешно изменён!',
                                     'queue_list': queue_list, 'queue_position': 0, 'queue_answers': [],
                                     'edit_profile': int(args[1]), 'queue_docs': '', 'last_queue_message': ''})

                                current_queue(update, context, user)

                        if args[2] == 'choose':
                            order = Order.get(id=int(args[1]))
                            order.status = 'Исполнитель выбран'

                            context.bot.edit_message_text(chat_id=CHANNEL_ID, message_id=order.channel_message,
                                                          text=get_order(order.id), reply_markup=None,
                                                          parse_mode=telegram.ParseMode.HTML)

                            worker_id = args[3]

                            for w in order.worker_id.split(','):
                                if w != worker_id and w != '':
                                    wr = User.get(id=int(w))
                                    text = 'К сожалению, по заказу #{} ({}) был выбран другой исполнитель или заказ был отменён.'.format(order.id, order.subject)
                                    context.bot.send_message(chat_id=wr.user_id, text=text, parse_mode=telegram.ParseMode.HTML)

                            order.worker_id = args[3]

                            wort = User.get(id=int(args[3]))

                            print(args)

                            text = 'Вы успешно выбрали исполнителя {} для заказа #{} ({}). Ожидайте создание чата.'.format(get_name(wort, True), order.id, order.subject)
                            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

                            text = 'Пользователь ' + get_name(user, True) + ' выбрал исполнителя ' + get_name(wort, True) + ' для заказа #' + str(order.id)
                            admins = list(select(u for u in User if u.status == 'admin'))
                            for admin in admins:
                                context.bot.send_message(chat_id=admin.user_id, text=text + '!', parse_mode=telegram.ParseMode.HTML)

                            text = 'Вас выбрали исполнителем для заказа #{} ({}). Ожидайте создание чата.'.format(order.id, order.subject)
                            context.bot.send_message(chat_id=wort.user_id, text=text, parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'withdrawconfirm':
                            buttons = [InlineKeyboardButton('Завершить', callback_data='@' + args[1] + '@withdrawdone@' + args[3])]

                            markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                                       footer_buttons=None)
                            reply_markup = InlineKeyboardMarkup(markup)

                            message = update.callback_query.message
                            context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                          message_id=message.message_id,
                                                          text=message.text + '\n👌 ОДОБРЕНО',
                                                          parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup, )

                            text = 'Ваша заявка на <b>вывод ' + args[3] + ' руб.</b> одобрена и будет выполнена в ближайшее время.'
                            context.bot.send_message(chat_id=int(args[1]), text=text, parse_mode=telegram.ParseMode.HTML)

                        if args[2] == 'withdrawdone':
                            # print(args)
                            # user = User.get(id=int(args[1]))
                            # print(user)
                            print(user.user_id)
                            user.balance -= int(args[3])

                            message = update.callback_query.message
                            context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message.message_id,
                                                          text=message.text + '\n👉 ЗАВЕРШЕНО', reply_markup=None,
                                                          parse_mode=telegram.ParseMode.HTML)

                            text = 'Ваша заявка на <b>вывод ' + args[3] + ' руб.</b> выполнена.'
                            context.bot.send_message(chat_id=user.user_id, text=text, parse_mode=telegram.ParseMode.HTML)
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Баланс пользователя ' + get_name(user, True) +
                                                     ' <b>уменьшен на ' + args[3] + ' руб.</b>', parse_mode=telegram.ParseMode.HTML)
    else:
        if query.data[0] == '@':
            args = query.data.split('@')
            if args[2] == 'take':
                myorder = Order.get(id=int(args[1]))
                wor = User.get(user_id=int(update.callback_query.from_user.id))
                if wor.status != 'worker':
                    text = 'Вы не являетесь исполнителем.'
                    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=text)
                    return
                if myorder and myorder.status == 'Поиск исполнителя':

                    workers = myorder.worker_id

                    if workers:
                        workers = workers.split(',')

                    if str(wor.id) in workers:
                        text = 'Вы уже отправили заявку на выполнение заказа #{} ({}). Ожидайте решение клиента.'.format(myorder.id, myorder.subject)
                        context.bot.send_message(chat_id=update.callback_query.from_user.id, text=text)
                        return

                    myorder.worker_id += str(wor.id) + ","
                    print(workers)

                    name = get_name(wor)

                    label = name + ' (id' + str(wor.id) + ')\n'
                    buttons = [InlineKeyboardButton('Профиль ' + label, callback_data='@' + str(wor.id) + '@showprofile'),
                        InlineKeyboardButton('Выбрать ' + label, callback_data='@' + args[1] + '@choose@' + str(wor.id)),
                    ]
                    markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                               footer_buttons=None)

                    usert = User.get(id=myorder.user_id)
                    name = get_name(user, True)

                    text = 'Пользователь {} отправил заявку на выполнение Вашего заказа #{} ({}).'.format(name, myorder.id, myorder.subject)
                    context.bot.send_message(chat_id=usert.user_id, text=text,
                                             reply_markup=InlineKeyboardMarkup(markup), parse_mode=telegram.ParseMode.HTML)

                    text = 'Заявка на выполнение заказа #{} ({}) успешно отправлена. Ожидайте решение клиента.'.format(myorder.id, myorder.subject)
                    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=text)
                else:
                    text = 'К сожалению, по заказу #{} ({}) был выбран другой исполнитель или заказ был отменён.'.format(myorder.id, myorder.subject)
                    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=text)

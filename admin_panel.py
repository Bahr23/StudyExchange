import datetime

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from menu import Menu
from models import *
from core import *
from menu import *
from transaction import Transaction
from user_panel import *

tr = Transaction


def adminhelp(update, context):
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
            if user.status == 'admin':
                text = '<b>Команды админ панели</b>\n' \
                       '\nУправление пользователями\n' \
                       '<code>/user</code> - информация о пользователе\n' \
                       '<code>/ubalance</code> - изменить баланс пользователя\n' \
                       '<code>/transfer</code> - трансфер средств от пользователя к пользователю\n' \
                       '<code>/setstatus</code> - изменить статус пользователя\n' \
                       '\nУправление заказами\n' \
                       '<code>/getorder</code> - информация о заказе\n' \
                       '<code>/newprice</code> - изменить цену заказ\n' \
                       '<code>/orderstatus</code> - изменить статус заказа\n' \
                       '<code>/reorder</code> - опубликовать заказ занаво\n' \
                       '<code>/activeorders</code> - информация об активных заказах\n' \
                       '<code>/orders</code> - все заказы\n' \
                       '\nТех. команды\n' \
                       '<code>/adminhelp</code> - справка по командам админ панели\n' \
                       '<code>/adminpanel</code> - вход (так же выход) в админ панель\n' \
                       '<code>/message</code> - отправить сообщение от имени бота пользователю\n' \
                       '<code>/channel</code> - отправить сообщение от имени бота в канал\n' \
                       '<code>/coupon</code> - создать купон или получить информацию о купоне\n' \
                       '<code>/delcoupon</code> - удалить купон\n'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                         parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def adminpanel(update, context):
    if update.message.chat.id > 0:
        user = get_user(update.message.from_user.id)
        mymenu = Menu()
        if user:
            if user.status == 'banned':
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
                context.bot.send_message(chat_id=update.effective_chat.id, text='error',
                                         reply_markup=reply_markup[0])
        else:
            start(update, context)


def channel(update, context):
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
            if user.status == 'admin':
                if context.args:
                    context.bot.send_message(chat_id=CHANNEL_ID, text=' '.join(context.args))
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
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
                            chat_id = user.user_id
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
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
                return
            if 'queue' in context.user_data.keys():
                if context.user_data['queue']:
                    current_queue(update, context, user)
                    return
            if user.status == 'admin':
                text = 'Используйте /ubalance user_id [-/+]amount'
                if context.args:
                    if len(context.args) >= 2:
                        user = User.get(id=int(context.args[0]))
                        if user:
                            amount = int(' '.join(context.args[1:]))
                            user.balance += amount
                            t = tr.new(type='Пополнение менеджером', bill_id='None', amount=int(amount), user_id=user.id,
                                       date=str(datetime.datetime.now())[0:19])
                            text = 'Баланс пользователя ' + get_name(user) + ' изменен на ' + str(amount) + 'р.'

                            if amount > 0:
                                utext = f'Ваш баланс пополнен на { str(amount)} руб. 💰'
                            else:
                                utext = f'Ваш баланс уменьшен на {str(abs(amount))} руб. 💰'
                            context.bot.send_message(chat_id=user.user_id, text=utext)
                        else:
                            text = 'Пользователь с id ' + context.args[0] + ' не найден'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)


            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def user(update, context):
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
            if user.status == 'admin':
                try:
                    id = int(context.args[0])
                    find_user = User.get(id=id)
                    if find_user:
                        mymenu = Menu()
                        buttons = [InlineKeyboardButton('Заказы', callback_data='@' + str(id) + '@userorders'),
                                   InlineKeyboardButton('Баланс', callback_data='@' + str(id) + '@userbalance'),
                                   InlineKeyboardButton('Сделать исполнителем', callback_data='@' + str(id) + '@makeworker'),
                                   InlineKeyboardButton('Забанить', callback_data='@' + str(id) + '@ban'),
                                   ]

                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                        reply_markup = InlineKeyboardMarkup(markup)
                        text = "@" + find_user.username + '\n' + get_profile(find_user.id)
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
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
                        if not u:
                            user_id = 0
                        else:
                            user_id = u.id
                        text = '<b>' + get_name(u) + '[' + str(user_id) + ']</b>\n'
                        text += get_order(id)
                        order = Order.get(id=id)

                        if order.promo != '0':
                            ctext = f'Купон: {order.promo}'
                        else:
                            ctext = f'Купон: None'
                        text += '\n' + ctext

                        if order.final_price:
                            ctext = f'Цена: {order.final_price}р.'
                        else:
                            ctext = f'Цена: None'
                        text += '\n' + ctext

                        chat = Chat.get(order_id=str(order.id))
                        if chat:
                            text += f'\nЧат: {chat.chat_link}'
                        else:
                            text += '\nЧат: None'

                        if ',' in order.worker_id:
                            workers = order.worker_id.split(',')[:-1]
                        else:
                            workers = [order.worker_id]
                        wtext = 'Исполнители:\n'
                        if workers != ['']:
                            # 'Текущие исполнители для заказа #' + args[1] + ':\n'
                            buttons = []

                            for w in workers:
                                wor = User.get(id=int(w))
                                label = wor.first_name + ' (' + str(wor.id) + ')\n'
                                wtext += label

                        text += '\n' + wtext

                        mymenu = Menu()
                        if order.status != 'Завершён':
                            buttons = [InlineKeyboardButton('Одобрить', callback_data='@' + str(id) + '@push'),
                                       InlineKeyboardButton('Редактировать', callback_data='@' + str(id) + '@edit@list'),
                                        InlineKeyboardButton('Удалить', callback_data='@' + str(id) + '@del')]

                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                        reply_markup = InlineKeyboardMarkup(markup)

                    # if order:
                    #     if order.docs != 'Вложения не добавлены':
                    #         text += '\nВложения:\n' + order.docs

                    except Exception as e:
                        print(e)
                        text = 'Используйте /getorder Номер_заказа!'
                else:
                    text = 'Используйте /getorder Номер_заказа!'

                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                         reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        else:
            start(update, context)


@db_session
def orders(update, context):
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
                    text = 'Заказы не найдены'
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
                context.bot.send_message(chat_id=user.user_id, text=BANNED_TEXT)
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
                            utext = 'Ваш статус изменен на ' + context.args[1]

                            if context.args[1] == 'worker':
                                utext = 'Ваша заявка на роль исполнителя успешно одобрена. Можете приступать к работе!'

                            context.bot.send_message(chat_id=user.user_id, text=utext)
                        else:
                            text = 'Пользователь с id ' + context.args[0] + ' не найден'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def orderstatus(update, context):
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
            if user.status == 'admin':
                text = 'Используйте /orderstatus order_id status'
                if context.args:
                    if len(context.args) >= 2:
                        order = Order.get(id=int(context.args[0]))
                        if order:
                            status = ' '.join(context.args[1:])
                            if status in ['На проверке', 'Поиск исполнителя', 'Исполнитель выбран', 'Ожидает оплаты',
                                          'Оплачен']:
                                order.status = status
                                try:
                                    context.bot.edit_message_text(chat_id=CHANNEL_ID, message_id=order.channel_message,
                                                                  text=get_order(order.id), reply_markup=None,
                                                                  parse_mode=telegram.ParseMode.HTML)
                                except Exception as e:
                                    pass
                                chat = Chat.get(order_id=context.args[0])
                                text = f'Статус заказа с id {context.args[0]} изменен на {status}'
                            else:
                                text = "status должен принимать одно из значений \n\nНа проверке\nПоиск исполнителя" \
                                       "\nИсполнитель выбран\nОжидает оплаты\nОплачен" \
                                       "\n\nЗавершение заказа происходит вручную!"
                        else:
                            text = f'Заказ с id {context.args[0]} не найден!'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def coupon(update, context):
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
            if user.status == 'admin':
                if len(context.args) == 1:
                    coupon = Coupons.get(name=context.args[0])
                    if coupon:
                        text = 'Name - ' + coupon.name + '\nAmount - ' + str(coupon.amount) + \
                               '\nCount - ' + str(coupon.count)
                if len(context.args) == 3:
                    try:
                        name = context.args[0]
                        amount = int(context.args[1])
                        count = int(context.args[2])

                        coupon = Coupons.get(name=name)
                        if coupon:
                            text = 'Купон с этим названием уже существует'
                        else:
                            coupon = Coupons(name=name, amount=amount, count=count)
                            text = 'Вы успешно создали купон ' + name
                    except Exception as e:
                        print(e)
                        text = 'Error'

                if not context.args:
                    text = '/coupon coupon_name - получить информацию о купоне' \
                           '\n/coupon coupon_name amount count - создать новый купон' \
                           '\n/delcoupon coupon_name - удалить купон'

                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def delcoupon(update, context):
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
            if user.status == 'admin':
                if len(context.args) == 1:
                    coupon = Coupons.get(name=context.args[0])
                    if coupon:
                        delete(c for c in Coupons if c.name == context.args[0])
                        text = 'Купон ' + context.args[0] + ' удалён.'
                    else:
                        text = 'Купон ' + context.args[0] + ' не найден.'

                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def newprice(update, context):
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
            if user.status == 'admin':
                text = 'error'
                if len(context.args) == 2:
                    try:
                        chat = Chat.get(order_id=context.args[0])
                        chat.price = str(int(context.args[1]))
                        text = f'Цена заказа #{context.args[0]} изменена на {context.args[1]}р.!'
                    except:
                        text = 'Используйте /newprice order_id new_price'
                else:
                    text = 'Используйте /newprice order_id new_price'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def transfer(update, context):
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
            if user.status == 'admin':
                text = 'Используйте /transfer user_id worker_id amount'
                if context.args:
                    if len(context.args) >= 3:
                        try:
                            user = User.get(id=int(context.args[0]))
                            if not user:
                                raise Exception(f'Пользователь с id {context.args[0]} не был найден!')

                            worker = User.get(id=int(context.args[1]))
                            if not worker:
                                raise Exception(f'Испольнитель с id {context.args[1]} не был найден!')

                            amount = int(context.args[2])

                            if amount > user.balance:
                                raise Exception(f'У пользователя с id {context.args[0]} недостаточно средств')

                            user.balance -= amount

                            t = tr.new(type='Трансфер средств',
                                       bill_id='None', amount=int(amount),
                                       user_id=user.id,
                                       date=str(datetime.datetime.now())[0:19])

                            context.bot.send_message(chat_id=user.user_id,
                                                     text=f'Трансфер средств. Ваш баланс уменьшен на {amount}р.')

                            worker.balance += int(amount * 0.85)

                            t = tr.new(type='Пополнение по трансферу средств',
                                       bill_id='None', amount=int(amount * 0.9),
                                       user_id=worker.id,
                                       date=str(datetime.datetime.now())[0:19])

                            context.bot.send_message(chat_id=worker.user_id,
                                                     text=f'Трансфер средств. Ваш баланс пополнен на {amount}р.')

                            partner = User.get(id=Settings.get(key='partner_id').value)
                            partner.balance += int(amount * 0.05)

                            t = tr.new(type='Партнерская выплата за трансфер средств',
                                       bill_id='None', amount=int(amount * 0.033),
                                       user_id=partner.id,
                                       date=str(datetime.datetime.now())[0:19])

                            text = 'Трансфер прошел успешно!'

                        except Exception as e:
                            text = e.args[0]
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)


            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def activeorders(update, context):
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
            if user.status == 'admin':
                text = '1'

                payed_orders = list(select(o for o in Order if o.status == 'Оплачен'))
                wait_for_pay_orders =  list(select(o for o in Order if o.status == 'Ожидает оплаты'))
                wait_for_chat_orders =  list(select(o for o in Order if o.status == 'Исполнитель выбран'))
                wait_for_worker_orders =  list(select(o for o in Order if o.status == 'Поиск исполнителя'))

                count = len(payed_orders) + len(wait_for_pay_orders) + len(wait_for_chat_orders) \
                        + len(wait_for_worker_orders)
                price = 0

                for o in payed_orders + wait_for_pay_orders:
                    try:
                        price += o.final_price
                    except:
                        pass

                text = f'<b>Активные заказы</b>\nВсего заказов: {count}\nОбщая сумма: {price}р.\n'

                text += f'\n<i>Оплачен</i>'
                for o in payed_orders:
                    if o:
                        text += f'<code>\n{o.subject} #{o.id} ({o.deadline}) - {o.final_price}р.</code>'

                text += f'\n\n<i>Ожидает оплаты</i>'
                for o in wait_for_pay_orders:
                    if o:
                        text += f'<code>\n{o.subject} #{o.id} ({o.deadline}) - {o.final_price}р.</code>'

                text += f'\n\n<i>Исполнитель выбран</i>'
                for o in wait_for_chat_orders:
                    if o:
                        text += f'<code>\n{o.subject} #{o.id} ({o.deadline})</code>'

                text += f'\n\n<i>Поиск исполнителя</i>'
                for o in wait_for_worker_orders:
                    if o:
                        text += f'<code>\n{o.subject} #{o.id} ({o.deadline})</code>'

                context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                         parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Вы не являетесь админом')
        else:
            start(update, context)


@db_session
def reorder(update, context):
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
            markup = ''
            if user.status == 'admin':
                if len(context.args) == 1:
                    text = 'ok'
                    order = Order.get(id=int(context.args[0]))
                    if order:
                        order.status = 'Поиск исполнителя'
                        chat = Chat.get(order_id=str(order.id))
                        if chat:
                            chat.delete()
                        try:
                            context.bot.delete_message(chat_id=CHANNEL_ID, message_id=order.channel_message)
                        except Exception as e:
                            print(e)
                        mymenu = Menu()
                        text = get_order(order.id)
                        buttons = [InlineKeyboardButton('Взять заказ 👍', callback_data='@' + str(order.id) + '@take')]
                        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)


                        usert = User.get(id=int(order.user_id))

                        post = context.bot.send_message(chat_id=CHANNEL_ID, text=text,
                                                        reply_markup=InlineKeyboardMarkup(markup),
                                                        parse_mode=telegram.ParseMode.HTML)
                        post_link = 'https://t.me/StudyExchangeSPbPU/' + str(post.message_id)

                        order.channel_message = post.message_id

                        text = 'Заказ #{} ({}) успешно одобрен!'.format(order.id, order.subject)
                        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

                        text = 'Ваш заказ #{} ({}) одобрен и <a href="{}">опубликован</a> на канале!'.format(order.id,
                                                                                                             order.subject,
                                                                                                             post_link)
                        context.bot.send_message(chat_id=usert.user_id, text=text, parse_mode=telegram.ParseMode.HTML)
                    else:
                        text = f'Заказ №{context.args[0]} не найден!'
                else:
                    text = 'Используйте /reorder order_id'
            else:
                text = 'Вы не являетесь админом'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(markup))
        else:
            start(update, context)


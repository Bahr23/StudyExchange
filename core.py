import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from menu import Menu
from models import *
from pay import *


CHANNEL_ID = '-1001361464885'
MEDIA_ID = '-1001412307468'
BANNED_TEXT = 'Ваш аккаунт был заблокирован в сервисе StudyExchange!'

@db_session
def get_user(id):
    try:
        user = User.get(user_id=id)
        return user
    except Exception as e:
        return False


def get_name(user, id=False):
    if user:
        name = str(user.id)
        if user.first_name != 'не указано':
            name = user.first_name
            if user.last_name != 'не указано':
                name += ' ' + user.last_name
        else:
            if user.username != 'не указано':
                name = user.username
        if id:
            name = '<b>' + name
            name += '</b>[id<code>' + str(user.id) + '</code>]'
        return name
    return 'Unknown'


@db_session
def get_profile(id):
    user = User.get(id=id)
    if user:
        name = get_name(user)

        if user.status == 'user':
            status = 'клиент'

        if user.status == 'worker':
            status = 'исполнитель'

        if user.status == 'admin':
            status = 'менеджер'

        # if user.username:
        #     username = 'Никнейм: @' + user.username + '\n'
        # else:
        #     username = ''

        if user.last_order != 'не указано':
            last_order_date = user.last_order.split('.')
            last_order_date = last_order_date[2] + '.' + last_order_date[1] + '.' + last_order_date[0]
            last_order = '\nДата последнего заказа: ' + last_order_date + '\n'
        else:
            last_order = ''

        reg = user.registration_date.split('.')
        reg = reg[2] + '.' + reg[1] + '.' + reg[0]


        text = '{name} [id<code>{id}</code>]\n\nСтатус: {status}\nДата регистрации: ' \
               '{registration_date}\n\nОбразование: {education}\nГород: {city}\nВозраст: ' \
               '{age}\n\nЗавершенные заказы: {orders_number}{last_order}\nРейтинг исполнителя: {rate}' \
               '\n'.format(name=name, id=user.id, status=status, registration_date=reg,
                                                                education=user.education, city=user.city, age=user.age,
                                                                orders_number=user.orders_number,
                                                                last_order=last_order, rate=user.rate)
        return text
    else:
        return False


@db_session
def get_order(id):
    order = Order.get(id=id)
    if order:
        if order.faculty != 'Пропустить':
            faculty = '\nФакультет - ' + order.faculty.lower()
        else:
            faculty = ''

        if order.departament != 'Пропустить':
            departament = '\nКафедра - ' + order.departament.lower()
        else:
            departament = ''

        if order.teacher != 'Пропустить':
            teacher = '\nПреподователь - ' + order.teacher.lower()
        else:
            teacher = ''

        text = 'Номер заказа: ' + str(order.id) + '\nСтатус: ' + order.status.lower() + '\nПредмет: ' + order.subject.lower() + '\nТип: ' + \
               order.type.lower() + faculty + departament + teacher + '\nСроки: ' + order.deadline.lower() + '\nЦена: ' + order.price.lower() + '\nОписание: ' + \
               order.description
        return text
    else:
        return False


@db_session
def delete_order(id):
    order = Order.get(id=id)
    if order:
        delete(o for o in Order if o.id == id)
        return 'Заказ №' + str(id) + ' удален.'
    else:
        return 'Заказ номер ' + str(id) + ' не найден.'


def queue(update, context, user, ans=None):
    if update.callback_query:
        query = update.callback_query
        if not ans:
            ans = query.data
    else:
        if not ans:
            ans = update.message.text
    answer = {list(context.user_data['queue_list'][context.user_data['queue_position']].keys())[0]: ans}
    context.user_data['queue_answers'].append(answer)
    context.user_data['queue_position'] += 1
    if context.user_data['queue_position'] < len(context.user_data['queue_list']):
        current_queue(update, context, user)
    else:
        finish_queue(context.user_data['queue_name'], context.user_data['queue_answers'], update, context)
        context.user_data['queue'] = False
        if context.user_data['queue_finish']:
            text = context.user_data['queue_finish']
            mymenu = Menu()
            reply_markup = mymenu.get_menu(tag='#main#0')
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0])


def current_queue(update, context, user):
    if (context.user_data['queue_name'] == 'edit_order' or context.user_data['queue_name'] == 'edit_profile') and context.user_data['queue_position'] == 1:
        return
    text = list(context.user_data['queue_list'][context.user_data['queue_position']].values())[0]
    qmenu = context.user_data['queue_list'][context.user_data['queue_position']]['menu']

    if qmenu:
        mymenu = Menu()
        reply_markup = mymenu.get_menu(tag=qmenu)[0]
    else:
        reply_markup = None
    if context.user_data['last_queue_message'] == text:
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    context.user_data.update({'last_queue_message': text})



@db_session
def finish_queue(name, answers, update=None, context=None):
    mymenu = Menu()
    if update.callback_query:
        query = update.callback_query
        user = get_user(update.callback_query.message.chat.id)
    else:
        user = get_user(update.message.from_user.id)

    if name == "new_order":
        subject = list(answers[0].values())[0]
        order_type = list(answers[1].values())[0]
        description = list(answers[2].values())[0]
        deadline = list(answers[3].values())[0]
        price = list(answers[4].values())[0]
        faculty = list(answers[5].values())[0]
        departament = list(answers[6].values())[0]
        teacher = list(answers[7].values())[0]
        docs = list(answers[8].values())[0]
        promo = list(answers[9].values())[0]

        coupon = Coupons.get(name=promo)

        if not coupon:
            promo = '0'

        try:
            docs = docs.split(', ')
            media_group = []
            for d in docs:
                if d != '':
                    media_group.append(InputMediaPhoto(media=d.replace(',', '')))
            url = 'https://t.me/StudyExchangeMedia/' + str(context.bot.send_media_group(chat_id=MEDIA_ID, media=media_group)[0].message_id)
        except Exception as e:
            url = 'Вложения не добавлены'

        order = Order(user_id=user.id, status='В обработке', subject=subject, type=order_type, faculty=faculty,
                      departament=departament, teacher=teacher, description=description,
                      deadline=deadline, price=price, worker_id='', docs=url, promo=promo)

        # # Оповещение пользователя
        # text = 'Ваш заказ добавлен в обработку и в скором времени будет опубликован'
        # context.bot.send_message(chat_id=user.user_id, text=text)

        # Оповещение админов
        orders = select(o for o in Order)
        id = int(list(orders)[-1].id)
        text = 'Пользователь ' + get_name(user, True) + ' создал заказ №' + str(id) + '\n'
        text += get_order(id)
        mymenu = Menu()
        buttons = [InlineKeyboardButton('Одобрить', callback_data='@' + str(id) + '@push'),
                   InlineKeyboardButton('Удалить', callback_data='@' + str(id) + '@del')]

        markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
        reply_markup = InlineKeyboardMarkup(markup)

        admins = list(select(u for u in User if u.status == 'admin'))

        if order.docs:
            text += '\nВложения:\n' + order.docs

        for admin in admins:
            context.bot.send_message(chat_id=admin.user_id, text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)

    if name == "edit_order":
        myorder = Order.get(id=context.user_data['edit_order'])
        key = list(answers[0].keys())[0]
        value = list(answers[0].values())[0]
        exec('myorder.' + key + " = '" + value + "'")
        context.user_data.update({'edit_order': None})

    if name == "edit_profile":
        user = User.get(id=context.user_data['edit_profile'])
        key = list(answers[0].keys())[0]
        value = list(answers[0].values())[0]
        if key == 'age':
            try:
                age = int(value)
                if age < 1:
                    raise
                exec('user.' + key + " = '" + value + "'")

            except Exception as e:
                text = "Введите число больше 0!"
                context.user_data.update({'queue_finish': False})
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        if key == 'education':
            try:
                education = str(value)
                for s in education:
                    if not s.isalpha() and s != '-':
                        raise
                exec('user.' + key + " = '" + value + "'")

            except Exception as e:
                text = "В поле «Образование» должные содержаться только буквы!"
                context.user_data.update({'queue_finish': False})
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        if key == 'city':
            try:
                city = str(value)
                for s in city:
                    if not s.isalpha() and s != '-':
                        raise
                exec('user.' + key + " = '" + value + "'")

            except Exception as e:
                text = "В поле «Город» должные содержаться только буквы!"
                context.user_data.update({'queue_finish': False})
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if name == "balance":
        try:
            sum = int(answers[0]['sum'])
            if sum > 0:
                text = 'Ссылка на оплату: '
                link = paylink(user.id, sum)
                text += link
            else:
                text = "Сумма пополнения должна быть болье 0!"
        except Exception as e:
            text = 'Сумма пополнения должна быть числом!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if name == "withdraw":
        try:
            sum = int(answers[0]['sum'])
            bank = answers[1]['bank']
            card = answers[2]['card']
            if sum <= int(user.balance):
                sum2 = sum * 0.97
                text = '<b>Пользователь ' + get_name(user) + '[' + str(user.id) + ']' + ' запрашивает вывод:</b>\n' \
                                                                                        '1. Сумма без комисси - ' + str(sum) + \
                       ' руб.\n  - Сумма с учетом комисси - ' + str(sum2) + ' руб\n2. Банк - ' + str(bank) + '\n3. Реквизиты - ' + str(card)

                buttons = [InlineKeyboardButton('Одобрить', callback_data='@' + str(user.user_id) + '@withdrawconfirm@' + str(sum)),
                           InlineKeyboardButton('Завершить', callback_data='@' + str(user.user_id) + '@withdrawdone@' + str(sum))]

                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                reply_markup = InlineKeyboardMarkup(markup)

                admins = list(select(u for u in User if u.status == 'admin'))
                for admin in admins:
                    context.bot.send_message(chat_id=admin.user_id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Ваша заявка на вывод отправлена на рассмотрение.')
            else:
                text = 'Ваша заявка отклонена. На балансе недостаточно средств.'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        except Exception as e:
            text = 'Сумма вывода должна быть числом!'

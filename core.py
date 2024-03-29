import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Bot, ReplyKeyboardMarkup

from menu import Menu
from models import *
from pay import *


CHANNEL_ID = '-1001291038829'
MEDIA_ID = '-1001412307468'
# CHANNEL_ID = '-489614808'
# MEDIA_ID = '-438856140'
BANNED_TEXT = 'К сожалению, Ваш аккаунт был заблокирован 😔'


with db_session:
    TOKEN = Settings.get(key='tg_token').value

bot = Bot(token=TOKEN)


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
            name = '<b>{} (id{})</b>'.format(name, user.id)
        return name
    return 'Unknown'


@db_session
def get_profile(id):
    user = User.get(id=id)
    if user:
        name = get_name(user)

        if user.status == 'user':
            status = 'клиент'
            rate = ''

        if user.status == 'worker':
            status = 'исполнитель'
            rate = 'Рейтинг: ' + str(user.rate)

        if user.status == 'admin':
            status = 'менеджер'
            rate = ''

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

        about = user.about
        if not about:
            about = 'не указано'

        reg = user.registration_date.split('.')
        reg = reg[2] + '.' + reg[1] + '.' + reg[0]

        text = '<b>{name} (id{id})</b>\n\nСтатус: {status}\nДата регистрации: ' \
               '{registration_date}\n\nОбразование: {education}\nГород: {city}\nВозраст: ' \
               '{age}\n\nО себе: {about}\n\nЗавершённые заказы: {orders_number}{last_order}\n{rate}' \
               '\n'.format(name=name, id=user.id, status=status, registration_date=reg,
                                                                education=user.education, city=user.city, age=user.age,
                                                                orders_number=user.orders_number,
                                                                last_order=last_order, rate=rate, about=about)
        return text
    else:
        return False


@db_session
def get_order(id):
    o = Order.get(id=id)
    if o:
        emoji_status = {
            'На проверке': '🔎',
            'Поиск исполнителя': '📢',
            'Исполнитель выбран': '👨‍🎓',
            'Ожидает оплаты': '⏳',
            'Оплачен': '💰',
            'Завершён': '✅',
        }

        try:
            status = '{st} {emoji}'.format(st=o.status, emoji=emoji_status[o.status])
        except Exception as e:
            status = o.status

        price = o.price if o.price[-1] == '.' else (o.price + '.')
        description = o.description if o.description[-1] == '.' else (o.description + '.')
        docs = '' if o.docs == 'Вложения не добавлены' else o.docs

        extra_list = [x for x in (o.faculty, o.departament, o.teacher) if x != 'Пропустить']
        # extra_info = ', '.join(extra_list) + ('.\n' if len(extra_list) else '')
        extra_info = ', '.join(extra_list)
        if extra_info:
            if extra_info[-1] != '.':
                extra_info += '.\n'
            else:
                extra_info += '\n'


        return '<b>Заказ #{id} ({subject})</b>\n{status}\n\n{type}, {deadline}, {price}\n{extra_info}\n{description}\n\n{docs}'.format(
            id=o.id,
            subject=o.subject,
            status=status,
            type=o.type,
            deadline=o.deadline.lower(),
            price=price.lower(),
            extra_info=extra_info,
            description=description,
            docs=docs)
    else:
        return False


@db_session
def get_requisites(user_id, req):
    requisites = User.get(id=user_id).requisites
    if requisites:
        requisites = requisites.split(',')[req]
        if requisites:
            return requisites
        else:
            return None
    else:
        return None

@db_session
def delete_order(o_id):
    order = Order.get(id=o_id)
    if order:
        delete(o for o in Order if o.id == o_id)
        return 'Заказ #' + str(o_id) + ' успешно удалён.'
    else:
        return 'Заказ #' + str(o_id) + ' не найден.'


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
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup[0], parse_mode=telegram.ParseMode.HTML,)


def current_queue(update, context, user):
    if (context.user_data['queue_name'] == 'edit_order' or context.user_data['queue_name'] == 'edit_profile') and context.user_data['queue_position'] == 1:
        return
    text = list(context.user_data['queue_list'][context.user_data['queue_position']].values())[0]
    qmenu = context.user_data['queue_list'][context.user_data['queue_position']]['menu']

    if qmenu:
        if qmenu == 'clear':
            reply_markup = telegram.ReplyKeyboardRemove()
        else:
            if qmenu[0] == 'r':
                print(qmenu)
                req = qmenu.split('_')
                btn_text = get_requisites(req[0][1:], int(req[1]))
                mymenu = Menu()
                if btn_text:
                    custom_keyboard = [[btn_text]]
                    reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
                else:
                    reply_markup = mymenu.get_menu(tag='#main#0')[0]
            else:
                mymenu = Menu()
                reply_markup = mymenu.get_menu(tag=qmenu)[0]
    else:
        reply_markup = None
    if context.user_data['last_queue_message'] == text:
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML,)
    context.user_data.update({'last_queue_message': text})


@db_session
def new_order_db(user_id, subject, order_type, description, deadline, price, faculty, departament, teacher, url, promo):
    order = Order(user_id=user_id, status='На проверке', subject=subject, type=order_type, faculty=faculty,
                  departament=departament, teacher=teacher, description=description,
                  deadline=deadline, price=price, worker_id='', docs=url, promo=promo)
    commit()
    return order


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

        order = new_order_db(user.id, subject, order_type, description, deadline, price, faculty, departament, teacher, url, promo)
        print(order)
        id = order.id
        print(id)

        # # Оповещение пользователя
        # text = 'Ваш заказ добавлен в обработку и в скором времени будет опубликован'
        # context.bot.send_message(chat_id=user.user_id, text=text)

        # Оповещение админов
        # orders = select(o for o in Order)
        # id = int(list(orders)[-1].id)
        text = 'Пользователь ' + get_name(user, True) + ' создал заказ #' + str(id) + '\n'
        text += get_order(id)
        mymenu = Menu()
        buttons = [InlineKeyboardButton('Одобрить', callback_data='@' + str(id) + '@push'),
                   InlineKeyboardButton('Редактировать', callback_data='@' + str(id) + '@edit@list'),
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
                text = "Введите число больше нуля!"
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
                text = 'В поле "Образование" могут находиться только буквы!'
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
                text = 'В поле "Город" могут находиться только буквы!'
                context.user_data.update({'queue_finish': False})
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        if key == 'about':
            try:
                about = str(value)
                if len(about) >= 120:
                    raise
                exec('user.' + key + " = '" + value + "'")

            except Exception as e:
                text = 'Поле "О себе" должно содержать не более 120 символов!'
                context.user_data.update({'queue_finish': False})
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if name == "depositsber":
        try:
            sum = int(answers[0]['sum'])
            if sum > 0:
                text = f'Переведите ровно {sum} руб. на карту СберБанка 👇\n\n<b><pre>5469 5500 4083 4357</pre>\nАлексей Олегович К.</b>\n\n⚠️ Комментарий к переводу указывать не надо.'
                buttons = [
                    InlineKeyboardButton('Оплатил 👍', callback_data='@' + str(user.id) + '@donedepositsber' + '@' + str(sum))]

                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                           footer_buttons=None)
                reply_markup = InlineKeyboardMarkup(markup)
            else:
                text = "Сумма пополнения должна быть больше нуля!"
                reply_markup = None
        except Exception as e:
            text = 'Сумма пополнения должна быть числом!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text,  parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)

    if name == "deposittin":
        try:
            sum = int(answers[0]['sum'])
            if sum > 0:
                text = f'Переведите ровно {sum} руб. на карту банка Тинькофф 👇\n\n<b><pre>5536 9138 8428 9543</pre> \nАлексей Олегович К.</b>\n\n⚠️ Комментарий к переводу указывать не надо.'
                buttons = [
                    InlineKeyboardButton('Оплатил 👍', callback_data='@' + str(user.id) + '@donedeposittin' + '@' + str(sum))]

                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                           footer_buttons=None)
                reply_markup = InlineKeyboardMarkup(markup)
            else:
                text = "Сумма пополнения должна быть больше нуля!"
                reply_markup = None
        except Exception as e:
            text = 'Сумма пополнения должна быть числом!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text,  parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)

    if name == "balance":
        try:
            sum = int(answers[0]['sum'])
            if sum > 0:
                text = 'Перейдите на страницу оплаты 👉 '
                link = paylink(user.id, sum)
                text += link
            else:
                text = "Сумма пополнения должна быть больше нуля!"
        except Exception as e:
            text = 'Сумма пополнения должна быть числом!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if name == "withdrawsber":
        print(answers)
        try:
            sum = int(answers[1]['sum'])
            bank = 'СберБанк'
            card = answers[0]['card']
            if sum <= int(user.balance):
                user.balance -= sum
                sum2 = sum * 0.97
                text = '<b>Пользователь ' + get_name(user) + '[' + str(user.id) + ']' + ' запрашивает вывод:</b>\n' \
                                                                                        '1. Сумма без комисси - ' + str(sum) + \
                       ' руб.\n  - Сумма с учетом комисси - ' + str(sum2) + ' руб\n2. Банк - ' + str(bank) + '\n3. Реквизиты - ' + str(card)

                if user.requisites is None:
                    user.requisites = f'{card},,'
                else:
                    requisites = user.requisites.split(',')
                    requisites[0] = card
                    user.requisites = f'{requisites[0]},{requisites[1]},{requisites[2]}'

                buttons = [InlineKeyboardButton('Отклонить', callback_data='@' + str(user.user_id) + '@withdrawreject@' + str(sum)),
                           InlineKeyboardButton('Одобрить', callback_data='@' + str(user.user_id) + '@withdrawconfirm@' + str(sum)),
                           InlineKeyboardButton('Завершить', callback_data='@' + str(user.user_id) + '@withdrawdone@' + str(sum))]

                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                reply_markup = InlineKeyboardMarkup(markup)

                admins = list(select(u for u in User if u.status == 'admin'))
                for admin in admins:
                    context.bot.send_message(chat_id=admin.user_id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Ваша заявка на вывод средств успешно отправлена. Ожидайте решение <a href="https://t.me/AlexStudyX">менеджера</a> ⏳', parse_mode=telegram.ParseMode.HTML)
            else:
                text = 'Ваша заявка отклонена: на балансе недостаточно средств.'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        except Exception as e:
            print(e)
            text = 'Сумма вывода должна быть числом!'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if name == "withdrawstin":
        print(answers)
        try:
            sum = int(answers[1]['sum'])
            bank = 'Тинькофф'
            card = answers[0]['card']
            if sum <= int(user.balance):
                user.balance -= sum
                sum2 = sum * 0.97
                text = '<b>Пользователь ' + get_name(user) + '[' + str(user.id) + ']' + ' запрашивает вывод:</b>\n' \
                                                                                        '1. Сумма без комисси - ' + str(sum) + \
                       ' руб.\n  - Сумма с учетом комисси - ' + str(sum2) + ' руб\n2. Банк - ' + str(bank) + '\n3. Реквизиты - ' + str(card)

                if user.requisites is None:
                    user.requisites = f',{card},'
                else:
                    requisites = user.requisites.split(',')
                    requisites[1] = card
                    user.requisites = f'{requisites[0]},{requisites[1]},{requisites[2]}'

                buttons = [InlineKeyboardButton('Отклонить', callback_data='@' + str(user.user_id) + '@withdrawreject@' + str(sum)),
                           InlineKeyboardButton('Одобрить', callback_data='@' + str(user.user_id) + '@withdrawconfirm@' + str(sum)),
                           InlineKeyboardButton('Завершить', callback_data='@' + str(user.user_id) + '@withdrawdone@' + str(sum))]

                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                reply_markup = InlineKeyboardMarkup(markup)

                admins = list(select(u for u in User if u.status == 'admin'))
                for admin in admins:
                    context.bot.send_message(chat_id=admin.user_id, text=text, parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Ваша заявка на вывод средств успешно отправлена. Ожидайте решение <a href="https://t.me/AlexStudyX">менеджера</a> ⏳', parse_mode=telegram.ParseMode.HTML)
            else:
                text = 'Ваша заявка отклонена: на балансе недостаточно средств.'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        except Exception as e:
            print(e)
            text = 'Сумма вывода должна быть числом!'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if name == "withdrawother":
        print(answers)
        try:
            sum = int(answers[1]['sum'])
            bank = 'Другой банк'
            card = answers[0]['card']
            if sum <= int(user.balance):
                user.balance -= sum
                sum2 = sum * 0.97
                text = '<b>Пользователь ' + get_name(user) + '[' + str(user.id) + ']' + ' запрашивает вывод:</b>\n' \
                                                                                        '1. Сумма без комисси - ' + str(sum) + \
                       ' руб.\n  - Сумма с учетом комисси - ' + str(sum2) + ' руб\n2. Банк - ' + str(bank) + '\n3. Реквизиты - ' + str(card)

                if user.requisites is None:
                    user.requisites = f',,{card}'
                else:
                    requisites = user.requisites.split(',')
                    requisites[2] = card
                    user.requisites = f'{requisites[0]},{requisites[1]},{requisites[2]}'

                buttons = [InlineKeyboardButton('Отклонить', callback_data='@' + str(user.user_id) + '@withdrawreject@' + str(sum)),
                           InlineKeyboardButton('Одобрить', callback_data='@' + str(user.user_id) + '@withdrawconfirm@' + str(sum)),
                           InlineKeyboardButton('Завершить', callback_data='@' + str(user.user_id) + '@withdrawdone@' + str(sum))]

                markup = mymenu.build_menu(buttons=buttons, n_cols=1, header_buttons=None, footer_buttons=None)
                reply_markup = InlineKeyboardMarkup(markup)

                admins = list(select(u for u in User if u.status == 'admin'))
                for admin in admins:
                    context.bot.send_message(chat_id=admin.user_id, text=text, parse_mode=telegram.ParseMode.HTML,
                                             reply_markup=reply_markup)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Ваша заявка на вывод средств успешно отправлена. '
                                              'Ожидайте решение <a href="https://t.me/AlexStudyX">менеджера</a> ⏳',
                                         parse_mode=telegram.ParseMode.HTML)
            else:
                text = 'Ваша заявка отклонена: на балансе недостаточно средств.'
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        except Exception as e:
            print(e)
            text = 'Сумма вывода должна быть числом!'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

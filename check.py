import telegram
from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime
import time
import datetime

from telegram import Bot

from pay import *

from models import *
from transaction import *

with db_session:
    phone = Settings.get(key='phone').value
    token = Settings.get(key='token').value

    QIWI_PRIV_KEY = Settings.get(key='QIWI_PRIV_KEY').value

p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
tr = Transaction

with db_session:
    TOKEN = Settings.get(key='tg_token').value

bot = Bot(token=TOKEN)


def monitoring():
    print(bot.username + ' start checking Transactions!')
    while True:
        print('Checking Transactions is active!')
        check_chats()
        with db_session:
            bills = list(select(u for u in Bills))
            for b in bills:
                bi = p2p.check(bill_id=b.bill_id)
                expiration = time.mktime(time.strptime(b.expiration, '%Y-%m-%dT%H:%M:%S+03:00'))
                if expiration > time.time():
                    if bi.status == 'PAID':
                        comment = decomment(bi.comment).split('@')
                        pas = Settings.get(key='password').value
                        if comment[1] == pas:
                            user = User.get(id=int(comment[0]))
                            if user:
                                user.balance += int(float(bi.amount))
                                t = tr.new(type='Пополнение', bill_id=str(bi.bill_id), amount=int(float(bi.amount)), user_id=user.id, date=str(datetime.datetime.now())[0:19])
                                p2p.reject(bill_id=b.bill_id)
                                b.delete()
                                text = 'Ваш баланс пополнен на ' + str(int(float(bi.amount))) + ' руб. 💸'
                                bot.send_message(chat_id=user.user_id, text=text)
                else:
                    p2p.reject(bill_id=b.bill_id)
                    b.delete()
        time.sleep(5)


def check_chats():
    print('Checking Chats is active!')
    with db_session:
        chats = list(select(u for u in Chat))
        for c in chats:
            if c.status == 'wait':
                chat_members_count = bot.get_chat_members_count(chat_id=int(c.chat_id))
                if chat_members_count >= 4:
                    pintext = '⚠️ Перед началом работы обязательно ознакомьтесь с инструкцией:\n\n' \
                              '1. Обе стороны обговаривают все условия заказа, после чего клиент или исполнитель' \
                              ' должен написать "/price [<b>цена</b>]" в общий чат.\n2. Клиент вносит полную предоплату' \
                              ' через бота. Бот присылает сообщение об успешной оплате в общий чат. Только после' \
                              ' этого исполнитель приступает к работе.\n3. Для завершения работы исполнитель или' \
                              ' клиент должен написать "/done" в общий чат.\n\nЗа разрешение спорных ситуаций ' \
                              'отвечает менеджер, вызвать которого можно командой "/admin".'
                    pinid = bot.send_message(chat_id=int(c.chat_id), text=pintext, timeout=500,
                                             parse_mode=telegram.ParseMode.HTML, )
                    bot.pin_chat_message(chat_id=int(c.chat_id), message_id=pinid.message_id)
                    c.status = 'active'

monitoring()

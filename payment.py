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


def monitoring():
    with db_session:
        TOKEN = Settings.get(key='tg_token').value

    bot = Bot(token=TOKEN)

    print(bot.username + ' start cheeking Transactions!')

    while True:
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
        time.sleep(1)


monitoring()

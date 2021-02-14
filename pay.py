from cryptography.fernet import Fernet
from models import *
from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime

with db_session:
    phone = Settings.get(key='phone').value
    token = Settings.get(key='token').value
    QIWI_PRIV_KEY = Settings.get(key='QIWI_PRIV_KEY').value

p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)


@db_session
def paylink(user_id, sum):
    key = Settings.get(key='key').value
    password = Settings.get(key='password').value
    f = Fernet(key.encode('utf-8'))
    c = str(user_id) + '@' + password
    comment = f.encrypt(c.encode('utf-8')).decode('utf-8')
    new_bill = p2p.bill(amount=sum, lifetime=60, comment=comment)

    bill = Bills(bill_id=new_bill.bill_id, amount=new_bill.amount, status=new_bill.status,
                status_changed=new_bill.status_changed, creation=new_bill.creation,
                expiration=new_bill.expiration, comment=new_bill.comment)

    link = new_bill.pay_url
    return link


@db_session
def decomment(s):
    key = Settings.get(key='key').value
    f = Fernet(key.encode('utf-8'))
    return f.decrypt(s.encode('utf-8')).decode('utf-8')

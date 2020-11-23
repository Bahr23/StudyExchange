import time

from models import *


class Transaction:
    @staticmethod
    def new(type, bill_id, amount, user_id, date):
        # self.type = type
        # self.bill_id = bill_id
        # self.amount = amount
        # self.user_id = user_id
        # self.date = date
        with db_session:
            return Transactions(type=type, bill_id=bill_id, amount=amount, user_id=user_id, date=date)

    @staticmethod
    def get(id):
        with db_session:
            t = Transactions.get(id=int(id))
        if t:
            text = t.date + ' | ' + str(t.amount) + 'р | ' + t.type + '[' + str(t.id) + ']'
        else:
            text = 'Транзакция с id ' + str(id) + ' не найдена'
        return text


# tr = Transaction
# for i in range(0, 5):
#     t = tr.new(type='DEPOSIT', bill_id='3131331-3131', amount=100, user_id=455788012, date=time.strftime('%d.%M.%Y'))
#
# print(tr.get(t.id))

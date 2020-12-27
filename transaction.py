import datetime

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
            datetime = t.date.split(' ')
            date = datetime[0].split('-')
            date = f"{date[2]}.{date[1]}.{date[0]}"
            text = '{} | {} | {} руб.'.format(date + ' ' + datetime[1][:-3], t.type, t.amount)
        else:
            text = 'Транзакция с id ' + str(id) + ' не найдена'
        return text


# tr = Transaction
# for i in range(0, 5):
#     t = tr.new(type='DEPOSIT', bill_id='3131331-3131', amount=100, user_id=455788012, date=time.strftime('%d.%M.%Y'))
#
# print(tr.get(t.id))

# print(str(datetime.datetime.now())[0:19])
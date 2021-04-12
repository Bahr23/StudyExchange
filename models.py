import os
import re
from urllib.parse import urlparse

from pony.orm import *

db = Database()

# db.bind(provider='postgres', user='postgres', password='', host='localhost', database='')

db_url = urlparse(os.environ['DATABASE_URL'])
args = re.split('[:@]', db_url.netloc)
db.bind(provider=db_url.scheme, user=args[0], password=args[1], host=args[2], port=args[3], database=db_url.path[1:])


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Required(int)
    status = Optional(str)
    first_name = Required(str)
    last_name = Optional(str)
    username = Optional(str)
    vk_id = Optional(int)
    age = Optional(str)
    education = Optional(str)
    city = Optional(str)
    registration_date = Optional(str)
    last_order = Optional(str)
    orders_number = Optional(str)
    workers_orders = Optional(int)
    rate = Optional(float)
    points = Optional(int)
    rated_orders = Optional(int)
    balance = Required(int)
    wanted = Optional(bool)
    requisites = Optional(str)


class Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Required(int)
    status = Required(str)
    subject = Required(str)
    type = Required(str)
    faculty = Required(str)
    departament = Required(str)
    teacher = Required(str)
    description = Required(str)
    deadline = Required(str)
    price = Required(str)
    worker_id = Optional(str)
    docs = Optional(str)
    promo = Optional(str)
    channel_message = Optional(int)


class Settings(db.Entity):
    id = PrimaryKey(int, auto=True)
    key = Required(str)
    value = Optional(str)


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    chat_id = Optional(float)
    price = Optional(str)
    user_id = Optional(str)
    worker_id = Optional(str)
    order_id = Optional(str)
    worker_yes = Optional(int)
    user_yes = Optional(int)
    price_msg = Optional(int)
    done_msg = Optional(int)


class Bills(db.Entity):
    id = PrimaryKey(int, auto=True)
    bill_id = Required(str)
    amount = Required(float)
    status = Required(str)
    status_changed = Required(str)
    creation = Required(str)
    expiration = Required(str)
    comment = Required(str)


class Transactions(db.Entity):
    id = PrimaryKey(int, auto=True)
    type = Required(str)
    bill_id = Required(str)
    amount = Required(int)
    user_id = Required(int)
    date = Required(str)


class Coupons(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    amount = Required(int)
    count = Required(int)


db.generate_mapping(create_tables=True)

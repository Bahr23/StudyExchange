import time

from core import *

# bot.send_message(chat_id=455788012, text='test')

# 0 - console input, 1 - write in this file
mode = 0

user_status = 'admin'
text = 'Test text'
сooldown = 3

print('Выберите режим [0/1] \n0 - Данные водятся из консоли\n1 - Данные водятся из файла spam.py')

mode = int(input('mode = '))
print('=====================================')
if mode == 0:
    user_status = input("Введите статус пользователей для выборки ('all' - все пользователи) = ")
    text = input("Введите текст рассылки = ")

with db_session:
    if user_status == 'all':
        users = list(select(u for u in User))
    else:
        users = list(select(u for u in User if u.status == user_status))
print('=====================================')
print('Проверьте правельность данных и нажмите Enter')
print(f'user_status = {user_status}')
print(f'Найденно пользователей {len(users)}')
print(f'text = {text}')
print('...')
input()
print('=====================================')

n = 0
for u in users:
    try:
        bot.send_message(chat_id=u.user_id, text=text)
        n += 1
        print(f'{u.id} - отправлено')
        time.sleep(сooldown)
    except Exception as e:
        print(e)

print('=====================================')
print(f'Успешно отпарвлено {n} сообщений.')


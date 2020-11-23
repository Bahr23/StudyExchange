from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


class Menu:

    def __init__(self):
        self.menus = {
            'test': {
                'text': 'It`s test menu!',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("test1", callback_data="test1"),
                            InlineKeyboardButton("test2", callback_data="test2"),
                            InlineKeyboardButton("test3", callback_data="test3")],
                        'header': None,
                        'footer': InlineKeyboardButton("Далее", callback_data="#test#1"),
                        'n_cols': 4
                    },
                    {
                        'buttons': [
                            InlineKeyboardButton("test4", callback_data="test4"),
                            InlineKeyboardButton("test5", callback_data="test5"),
                            InlineKeyboardButton("test6", callback_data="test6")],
                        'header': InlineKeyboardButton("Назад", callback_data="#test#0"),
                        'footer': None,
                        'n_cols': 4
                    },
                ]
            },
            'main': {
                'text': 'Меню: \n/menu - Список комманд\n/myprofile - Мой профиль\n/profile - Посмотреть профиль '
                        'исполнителя\n/neworder - Сделать заказ\n/myorders '
                        '- Посмотреть свои заказы \n/order - Посмотреть определенный заказ '
                        'Номер_Заказа',
                'type': 'reply',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Меню", callback_data="/menu"),
                            InlineKeyboardButton("Новый заказ", callback_data="new_order"),
                            InlineKeyboardButton("Мои заказы", callback_data="my_orders"),
                            InlineKeyboardButton("Мой профиль", callback_data="myprofile"),
                            InlineKeyboardButton("Баланс", callback_data="balance"),
                            InlineKeyboardButton("Как это работает?", callback_data="faq"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 2
                    }
                ]
            },
            'chat': {
                'text': 'Чат меню:\n/price - утвердить цену\n/done - завершить заказ\n/admin - вызвать админа',
                'type': 'reply',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Утвердить цену", callback_data="/price"),
                            InlineKeyboardButton("Завершить заказ", callback_data="/done"),
                            InlineKeyboardButton("Вызвать админа", callback_data="/admin"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    }
                ]
            },
            'admin': {
                'text': 'Admin меню: \n/adminpanel - Поменять свой статус\n/channel - Отправить сообщение в '
                        'каннал\n/message - '
                        'Отправить сообщение пользователю\n/setstatus - Изменить статус пользователя\n/user - '
                        'Посмотреть информацию о пользователе\n/getorder - '
                        'Посмотреть информацию о заказе',
                'type': 'reply',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("/adminpanel", callback_data="admin"),
                            InlineKeyboardButton("/channel", callback_data="channel"),
                            InlineKeyboardButton("/message", callback_data="message"),
                            InlineKeyboardButton("/setstatus", callback_data="setstatus"),
                            InlineKeyboardButton("/user", callback_data="user"),
                            InlineKeyboardButton("/getorder", callback_data="getorder"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 2
                    }
                ]
            },
            'subject': {
                'text': 'Выберите предмет',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Предмет 1", callback_data="Предмет 1"),
                            InlineKeyboardButton("Предмет 2", callback_data="Предмет 2"),
                            InlineKeyboardButton("Предмет 3", callback_data="Предмет 3")],
                        'header': None,
                        'footer': InlineKeyboardButton("Далее", callback_data="#subject#1"),
                        'n_cols': 1
                    },
                    {
                        'buttons': [
                            InlineKeyboardButton("Предмет 4", callback_data="Предмет 4"),
                            InlineKeyboardButton("Предмет 5", callback_data="Предмет 5"),
                            InlineKeyboardButton("Предмет 6", callback_data="Предмет 6")],
                        'header': InlineKeyboardButton("Назад", callback_data="#subject#0"),
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'type': {
                'text': 'Выберите тип работы',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Тип 1", callback_data="Тип 1"),
                            InlineKeyboardButton("Тип 2", callback_data="Тип 2"),
                            InlineKeyboardButton("Тип 3", callback_data="Тип 3")],
                        'header': None,
                        'footer': InlineKeyboardButton("Далее", callback_data="#type#1"),
                        'n_cols': 1
                    },
                    {
                        'buttons': [
                            InlineKeyboardButton("Тип 4", callback_data="Тип 4"),
                            InlineKeyboardButton("Тип 5", callback_data="Тип 5"),
                            InlineKeyboardButton("Тип 6", callback_data="Тип 6")],
                        'header': InlineKeyboardButton("Назад", callback_data="#type#0"),
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'faculty': {
                'text': 'Укажите ваш факультет',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Пропустить", callback_data="Пропустить"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'departament': {
                'text': 'Укажите ваш факультет',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Пропустить", callback_data="Пропустить"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'teacher': {
                'text': 'Укажите ваш факультет',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Пропустить", callback_data="Пропустить"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols':1
                    },
                ]
            },
            'deadline': {
                'text': 'Укажите срок',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("1 день", callback_data="1 день"),
                            InlineKeyboardButton("До 2 дней", callback_data="До 2 дней"),
                            InlineKeyboardButton("До 3 дней", callback_data="До 3 дней"),
                            InlineKeyboardButton("До 7 дней", callback_data="До 7 дней")
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'price': {
                'text': 'Укажите цену',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("500 руб", callback_data="500 руб"),
                            InlineKeyboardButton("1000 руб", callback_data="1000 руб"),
                            InlineKeyboardButton("1500 руб", callback_data="1500 руб"),
                            InlineKeyboardButton("2000 руб", callback_data="2000 руб")
                        ],
                        'header': None,
                        'footer': InlineKeyboardButton("Договорная", callback_data="Договорная"),
                        'n_cols': 1
                    },
                ]
            },
            'done': {
                'text': "Все фотографии сохранены",
                'type': 'reply',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Готово", callback_data="!done"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'banks': {
                'text': "Выберите банк",
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("СберБанк", callback_data="Банк №1"),
                            InlineKeyboardButton("Тинькофф", callback_data="Банк №2"),
                            InlineKeyboardButton("Альфа-Банк", callback_data="Банк №3"),
                            InlineKeyboardButton("ВТБ", callback_data="Банк №4"),
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
        }

    def get_menu(self, tag):
        try:
            menu_name = tag.split("#")[1]
            menu_page = int(tag.split("#")[2])
            cur_menu = self.menus[menu_name]['body'][menu_page]
            markup = self.build_menu(buttons=cur_menu['buttons'],  n_cols=cur_menu['n_cols'],
                                  header_buttons=cur_menu['header'], footer_buttons=cur_menu['footer'])
            if self.menus[menu_name]['type'] == 'inline':
                return [InlineKeyboardMarkup(markup), self.menus[menu_name]['text']]

            if self.menus[menu_name]['type'] == 'reply':
                return [ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True), self.menus[menu_name]['text']]

        except Exception as e:
            return e

    @staticmethod
    def build_menu(buttons,
                   n_cols,
                   header_buttons=None,
                   footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu

    def order_buttons(self, id, workers=None):
        buttons = [
            InlineKeyboardButton('Редактировать', callback_data='@' + str(id) + '@edit@list'),
            InlineKeyboardButton('Оплатить', callback_data='@' + str(id) + '@buy'),
        ]

        if id:
            header_buttons = InlineKeyboardButton('Исполнители', callback_data='@' + str(id) + '@workers')
        else:
            header_buttons = None
        markup = self.build_menu(buttons=buttons, n_cols=1, header_buttons=header_buttons,
                                   footer_buttons=InlineKeyboardButton('❌ Удалить заказ ❌', callback_data='@' + str(id) + '@predel'))
        reply_markup = InlineKeyboardMarkup(markup)
        return reply_markup

    def edit_buttons(self, id):
        buttons = [
            InlineKeyboardButton('Изменить предмет', callback_data='@' + str(id) + '@edit@subject'),
            InlineKeyboardButton('Изменить тип работы', callback_data='@' + str(id) + '@edit@type'),
            InlineKeyboardButton('Изменить факультет', callback_data='@' + str(id) + '@edit@faculty'),
            InlineKeyboardButton('Изменить кафедру', callback_data='@' + str(id) + '@edit@departament'),
            InlineKeyboardButton('Изменить преподователя', callback_data='@' + str(id) + '@edit@teacher'),
            InlineKeyboardButton('Изменить описание', callback_data='@' + str(id) + '@edit@description'),
            InlineKeyboardButton('Изменить сроки', callback_data='@' + str(id) + '@edit@deadline'),
            InlineKeyboardButton('Изменить цену', callback_data='@' + str(id) + '@edit@price'),
        ]

        markup = self.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                 footer_buttons=None)
        reply_markup = InlineKeyboardMarkup(markup)
        return reply_markup

    def profile_buttons(self, id):
        buttons = [
            InlineKeyboardButton('Изменить образование', callback_data='@' + str(id) + '@profile@education'),
            InlineKeyboardButton('Изменить город', callback_data='@' + str(id) + '@profile@city'),
            InlineKeyboardButton('Изменить возраст', callback_data='@' + str(id) + '@profile@age'),
        ]

        markup = self.build_menu(buttons=buttons, n_cols=1, header_buttons=None,
                                 footer_buttons=None)
        reply_markup = InlineKeyboardMarkup(markup)
        return reply_markup

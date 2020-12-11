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
                'text': '/menu - список команд\n/neworder - новый заказ\n/myprofile - мой профиль\n'
                        '/myorders - мои заказы \n/balance - управление балансом\n/faq - как это работает?\n'
                        '/order <i>номер_заказа</i> - поиск заказа по его id\n'
                        '/profile <i>id_исполнителя</i> - поиск профиля исполнителя по его id',
                'type': 'reply',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Меню", callback_data="/menu"),
                            InlineKeyboardButton("Новый заказ", callback_data="new_order"),
                            InlineKeyboardButton("Мой профиль", callback_data="myprofile"),
                            InlineKeyboardButton("Мои заказы", callback_data="my_orders"),
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
                'text': 'Чат меню:\n/price - утвердить цену\n/done - завершить заказ\n/admin - вызвать менеджера',
                'type': 'reply',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Утвердить цену", callback_data="/price"),
                            InlineKeyboardButton("Завершить заказ", callback_data="/done"),
                            InlineKeyboardButton("Вызвать менеджера", callback_data="/admin"),
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
                        'Посмотреть информацию о заказе\n/ubalance - Изменить баланс пользователя',
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
                'text': 'Выберите предмет из списка или напишите свой:',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Математика", callback_data="Математика"),
                            InlineKeyboardButton("Программирование", callback_data="Программирование"),
                            InlineKeyboardButton("Физика", callback_data="Физика"),
                            InlineKeyboardButton("Химия", callback_data="Химия")],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'type': {
                'text': 'Выберите тип работы из списка или напишите свой:',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("Контрольная работа", callback_data="Контрольная работа"),
                            InlineKeyboardButton("Реферат", callback_data="Реферат"),
                            InlineKeyboardButton("Курсовая работа", callback_data="Курсовая работа"),
                            InlineKeyboardButton("Дипломная работа", callback_data="Дипломная работа"),
                            InlineKeyboardButton("Сдача экзамена", callback_data="Сдача экзамена")],
                        'header': None,
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
                'text': 'Выберите срок из списка или напишите свой:',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("1 день", callback_data="1 день"),
                            InlineKeyboardButton("До 7 дней", callback_data="До 7 дней"),
                            InlineKeyboardButton("До 30 дней", callback_data="До 30 дней"),
                            InlineKeyboardButton("До конца семестра", callback_data="До конца семестра")
                        ],
                        'header': None,
                        'footer': None,
                        'n_cols': 1
                    },
                ]
            },
            'price': {
                'text': 'Выберите цену из списка или напишите свою:',
                'type': 'inline',
                'body': [
                    {
                        'buttons': [
                            InlineKeyboardButton("500-1000 рублей", callback_data="500-1000 рублей"),
                            InlineKeyboardButton("1000-2000 руб.", callback_data="1000-2000 руб."),
                            InlineKeyboardButton("2000-3000 руб.", callback_data="2000-3000 руб."),
                            InlineKeyboardButton("3000-4000 руб.", callback_data="3000-4000 руб."),
                            InlineKeyboardButton("4000-5000 руб.", callback_data="4000-5000 руб."),
                            InlineKeyboardButton("По договоренности", callback_data="По договоренности")
                        ],
                        'header': None,
                        'footer': None,
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
            # InlineKeyboardButton('Редактировать', callback_data='@' + str(id) + '@edit@list'),
            InlineKeyboardButton('Оплатить', callback_data='@' + str(id) + '@buy'),
        ]

        if id:
            header_buttons = InlineKeyboardButton('Исполнители', callback_data='@' + str(id) + '@workers')
        else:
            header_buttons = None
        markup = self.build_menu(buttons=buttons, n_cols=1, header_buttons=header_buttons,
                                   footer_buttons=InlineKeyboardButton('❌ Отменить заказ ❌', callback_data='@' + str(id) + '@predel'))
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

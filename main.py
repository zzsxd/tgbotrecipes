#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
config_name = 'secrets.json'
xlsx_path = 'database.xlsx'
#####################################
import os
import telebot
import platform
import schedule
import time
import threading
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import TempUserData, DbAct
from db import DB


# def func():
#     data = db_actions.check_subscribe()
#     for i in data:
#         if int(time.time()) >= i[1]:
#             db_actions.ban_user(i[0])


# def schedule_check():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


def next_recept(user_id, buttons):
    temp_user_data.temp_data(user_id)[user_id][4] += 1
    index = temp_user_data.temp_data(user_id)[user_id][4]
    if index <= len(temp_user_data.temp_data(user_id)[user_id][2]) - 1:
        data = temp_user_data.temp_data(user_id)[user_id][2][index]
        bot.send_photo(chat_id=user_id,
                       caption=f'{data[1]}\n{data[2]}',
                       reply_markup=buttons.food_btns(), photo=data[0])
    else:
        bot.send_message(user_id, 'Рецепты закончились', reply_markup=buttons.back_btn())


def main():
    @bot.message_handler(commands=['start', 'admin'])
    def start_message(message):
        name_user = message.from_user.first_name
        user_id = message.from_user.id
        command = message.text.replace('/', '')
        buttons = Bot_inline_btns()
        db_actions.add_user(user_id, message.from_user.first_name, message.from_user.last_name,
                            f'@{message.from_user.username}')
        # db_actions.give_free_subscribe(user_id)
        # if db_actions.have_ban(user_id):
        if command == 'start':
            bot.send_message(message.chat.id,
                             f'Привет, {name_user}! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                             reply_markup=buttons.start_btns())
        elif db_actions.user_is_admin(user_id):
            if command == 'admin':
                bot.send_message(message.chat.id,
                                 f'Привет, {name_user}!',
                                 reply_markup=buttons.admin_btns())
        # else:
        #     bot.send_message(message.chat.id, 'У вас закончилась пробная подписка!\n',
        #                      reply_markup=buttons.buy_subscribe())

    @bot.message_handler(content_types=['text', 'photo'])
    def text(message):
        photo = message.photo
        user_input = message.text
        user_id = message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            if db_actions.have_ban(user_id):
                code = temp_user_data.temp_data(user_id)[user_id][0]
                match code:
                    case 0:
                        bot.send_message(message.chat.id, 'Выберите категорию!')
                        temp_user_data.temp_data(user_id)[user_id][0] = 1
                    case 1:
                        bot.send_message(message.chat.id, 'Название добавлено!')
                        bot.send_message(message.chat.id, 'Отправьте рецепт! (одим сообщением)')
                        temp_user_data.temp_data(user_id)[user_id][0] = 2
                    case 2:
                        bot.send_message(message.chat.id, 'Данные сохранены')
                    case 5:
                        if photo is not None:
                            temp_user_data.temp_data(user_id)[user_id][0] = 6
                            photo_id = photo[-1].file_id
                            photo_file = bot.get_file(photo_id)
                            photo_bytes = bot.download_file(photo_file.file_path)
                            temp_user_data.temp_data(user_id)[user_id][3][2] = photo_bytes
                            bot.send_message(user_id, 'Отправьте название блюда')
                        else:
                            bot.send_message(user_id, '❌Это не фото❌')
                    case 6:
                        if user_input is not None:
                            temp_user_data.temp_data(user_id)[user_id][3][3] = user_input
                            temp_user_data.temp_data(user_id)[user_id][0] = 7
                            bot.send_message(user_id, 'Введите рецепт')
                        else:
                            bot.send_message(user_id, '❌Это не текст❌')
                    case 7:
                        if user_input is not None:
                            temp_user_data.temp_data(user_id)[user_id][3][4] = user_input
                            db_actions.add_recept(temp_user_data.temp_data(user_id)[user_id][3])
                            temp_user_data.temp_data(user_id)[user_id][0] = None
                            bot.send_message(user_id, '✅Рецепт успешно добавлен✅')
                        else:
                            bot.send_message(user_id, '❌Это не текст❌')
            else:
                bot.send_message(message.chat.id, 'У вас закончилась пробная подписка!\n',
                                 reply_markup=buttons.buy_subscribe())

        else:
            bot.send_message(message.chat.id, 'Введите /start для запуска бота'
    )
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user = call.message.from_user.id
        button_text = call.message.text
        user_id = call.message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            if db_actions.have_ban(user_id):
                code = temp_user_data.temp_data(user_id)[user_id][0]
                if db_actions.user_is_admin(user_id):
                    if call.data == 'newrecept':
                        temp_user_data.temp_data(user_id)[user_id][0] = 3
                        bot.send_message(user_id, 'Выберите для какого возраста!',
                                         reply_markup=buttons.new_recept())
                    elif call.data[:6] == 'recept' and code == 3:
                        temp_user_data.temp_data(user_id)[user_id][0] = 4
                        temp_user_data.temp_data(user_id)[user_id][3][0] = call.data[6:]
                        bot.send_message(user_id, 'Выберите категорию!', reply_markup=buttons.new_recept2())
                    elif call.data[:5] == 'govno' and code == 4:
                        temp_user_data.temp_data(user_id)[user_id][0] = 5
                        temp_user_data.temp_data(user_id)[user_id][3][1] = call.data[5:]
                        bot.send_message(user_id, 'Отправьте обложку нового рецепта!')
                if call.data == "go":
                    temp_user_data.temp_data(user_id)[user_id][0] = 8
                    bot.send_message(call.message.chat.id,
                                     'Какой возраст у твоего ребенка?',
                                     reply_markup=buttons.age_btns())
                elif call.data[:3] == 'get' and code == 8:
                    temp_user_data.temp_data(user_id)[user_id][0] = 9
                    temp_user_data.temp_data(user_id)[user_id][1] = call.data[3:]
                    bot.send_message(call.message.chat.id,
                                     'Отлично! Теперь ты можешь выбрать прием пищи, и я отправлю рецепт в зависимости от возраста ребенка!',
                                     reply_markup=buttons.meal_btns())
                elif call.data[:3] == 'kal' and code == 9:
                    age = temp_user_data.temp_data(user_id)[user_id][1]
                    temp_user_data.temp_data(user_id)[user_id][2] = db_actions.get_recepts(age, call.data[3:])
                    temp_user_data.temp_data(user_id)[user_id][4] = -1
                    next_recept(user_id, buttons)
                elif call.data == 'nextrecipe':
                    next_recept(user_id, buttons)
                elif call.data == 'mainmenu':
                    temp_user_data.temp_data(user_id)[user_id][0] = None
                    bot.send_message(call.message.chat.id,
                                     f'Привет! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                                     reply_markup=buttons.start_btns())
                elif call.data == 'buy':
                    db_actions.check_subscribe()  # тут должна выдавать до какого времени активна подписка
                    bot.send_message(call.message.chat.id, 'Ваша подписка активна до: ',
                                     reply_markup=buttons.buy_subscribe())
            else:
                bot.send_message(call.message.chat.id, 'У вас закончилась пробная подписка!\n',
                                 reply_markup=buttons.buy_subscribe())
        elif call.data == 'export':
            db_actions.db_export_xlsx()
            bot.send_document(call.message.chat.id, open(xlsx_path, 'rb'))
            os.remove(xlsx_path)
        elif call.data == 'buy':
            bot.send_message('Ваша подписка активна до: ', reply_markup=buttons.buy_subscribe())
        elif call.data == 'month':
            bot.send_message('Вы подтверждаете следующие данные?\n'
                             'Подписка на 1 месяц\n'
                             'Цена: 299₽', reply_markup=buttons.confirm_data_month())
        elif call.data == '3month':
            bot.send_message('Вы подтверждаете следующие данные?\n'
                             'Подписка на 3 месяца\n'
                             'Цена: 599₽', reply_markup=buttons.confirm_data_3month())
        elif call.data == 'year':
            bot.send_message('Вы подтверждаете следующие данные?\n'
                             'Подписка на год\n'
                             'Цена: 1199₽', reply_markup=buttons.confirm_data_year())
        elif call.data == 'confirm1':
            pass  # отправка чека на оплату + добавление подписки при успешной оплате
        elif call.data == 'confirm2':
            pass  # отправка чека на оплату + добавление подписки при успешной оплате
        elif call.data == 'confirm3':
            pass  # отправка чека на оплату + добавление подписки при успешной оплате
        else:
            bot.send_message(user_id, 'Введите /start для запуска бота')

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, xlsx_path)
    # threading.Thread(target=schedule_check, args=()).start()
    # schedule.every().second.do(func)
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    admin_ids = config.get_config()['admins']
    main()

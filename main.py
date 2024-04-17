#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import types

config_name = 'secrets.json'
group_id = -1002138706559
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


def func():
    data = db_actions.check_subscribe()
    for i in data:
        if int(time.time()) >= int(i[1]):
            db_actions.ban_user(i[0])


def schedule_check():
    while True:
        schedule.run_pending()
        time.sleep(1)


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
        if command == 'start':
            bot.send_message(message.chat.id,
                                f'Привет, {name_user}! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                                reply_markup=buttons.start_btns())
        elif db_actions.user_is_admin(user_id):
            if command == 'admin':
                bot.send_message(message.chat.id,
                                 f'Привет, {name_user}!',
                                 reply_markup=buttons.admin_btns())

    @bot.message_handler(content_types=['text', 'photo'])
    def text(message):
        photo = message.photo
        user_input = message.text
        user_id = message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            if db_actions.user_is_admin(user_id):
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
                    case 10:
                        if user_input is not None:
                            topic_id = telebot.TeleBot.create_forum_topic(bot, chat_id=group_id,
                                                                          name=f'{message.from_user.first_name} '
                                                                               f'{message.from_user.last_name} ПОПОЛНЕНИЕ БАЛАНСА',
                                                                          icon_color=0x6FB9F0).message_thread_id
                            bot.forward_message(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.id,
                                                message_thread_id=topic_id)
                            bot.send_message(user_id, 'Отлично! Мы проверим информацию и вы получите доступ к боту!')
                            bot.send_message(group_id, message_thread_id=topic_id, text='Покупка подписка!\n\n'
                                                       'Покупка подписки на 1 месяц за 299 рублей!\n\n'
                                                       'Данные пользователя предоставлены выше, проверьте информацию и нажмите соответствующую кнопку.', reply_markup=buttons.manager_btns())
                    case 11:
                        if user_input is not None:
                            topic_id = telebot.TeleBot.create_forum_topic(bot, chat_id=group_id,
                                                                          name=f'{message.from_user.first_name} '
                                                                               f'{message.from_user.last_name} ПОПОЛНЕНИЕ БАЛАНСА',
                                                                          icon_color=0x6FB9F0).message_thread_id
                            bot.forward_message(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.id,
                                                message_thread_id=topic_id)
                            bot.send_message(user_id, 'Отлично! Мы проверим информацию и вы получите доступ к боту!')
                            bot.send_message(group_id, message_thread_id=topic_id, text='Покупка подписка!\n\n'
                                                       'Покупка подписки на 3 месяца за 599 рублей!\n\n'
                                                       'Данные пользователя предоставлены выше, проверьте информацию и нажмите соответствующую кнопку.', reply_markup=buttons.manager_btns())
                    case 12:
                        if user_input is not None:
                            topic_id = telebot.TeleBot.create_forum_topic(bot, chat_id=group_id,
                                                                          name=f'{message.from_user.first_name} '
                                                                               f'{message.from_user.last_name} ПОПОЛНЕНИЕ БАЛАНСА',
                                                                          icon_color=0x6FB9F0).message_thread_id
                            bot.forward_message(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.id,
                                                message_thread_id=topic_id)
                            bot.send_message(user_id, 'Отлично! Мы проверим информацию и вы получите доступ к боту!')
                            bot.send_message(group_id, message_thread_id=topic_id, text='Покупка подписка!\n\n'
                                                   'Покупка подписки на 1 год за 1199 рублей!\n\n'
                                                   'Данные пользователя предоставлены выше, проверьте информацию и нажмите соответствующую кнопку.', reply_markup=buttons.manager_btns())
        else:
            bot.send_message(message.chat.id, 'Введите /start для запуска бота')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            if not db_actions.have_ban(user_id):
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
                    bot.send_message(user_id,
                                     f'Привет! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                                     reply_markup=buttons.start_btns())
                elif call.data == 'buy':
                    db_actions.check_subscribe()  # тут должна выдавать до какого времени активна подписка
                    bot.send_message(user_id, 'Ваша подписка активна до: ',
                                     reply_markup=buttons.buy_subscribe())
                elif call.data == 'export':
                    db_actions.db_export_xlsx()
                    bot.send_document(call.message.chat.id, open(config.get_config()['xlsx_path'], 'rb'))
                    os.remove(config.get_config()['xlsx_path'])
                elif call.data == 'month':
                    bot.send_message(user_id, 'Вы подтверждаете следующие данные?\n'
                                     'Подписка на 1 месяц\n'
                                     'Цена: 299₽', reply_markup=buttons.confirm_data_month())
                elif call.data == '3month':
                    bot.send_message(user_id, 'Вы подтверждаете следующие данные?\n'
                                     'Подписка на 3 месяца\n'
                                     'Цена: 599₽', reply_markup=buttons.confirm_data_3month())
                elif call.data == 'year':
                    bot.send_message(user_id, 'Вы подтверждаете следующие данные?\n'
                                     'Подписка на 1 год\n'
                                     'Цена: 1199₽', reply_markup=buttons.confirm_data_year())
                elif call.data == 'confirm1':
                    bot.send_message(user_id, 'Подписка на 1 месяц, за 299₽\n\n'
                                              'Вам необходимо отправить 299₽ по номеру карты - \n\n'
                                              'После перевода вам необходимо отправить сообщение с вашими ФИО, мы проверим информацию и выдадим подписку!')
                    temp_user_data.temp_data(user_id)[user_id][0] = 10
                elif call.data == 'confirm2':
                    bot.send_message(user_id, 'Подписка на 3 месяца, за 599₽\n\n'
                                              'Вам необходимо отправить 599₽ по номеру карты - \n\n'
                                              'После перевода вам необходимо отправить сообщение с вашими ФИО, мы проверим информацию и выдадим подписку!')
                    temp_user_data.temp_data(user_id)[user_id][0] = 11
                elif call.data == 'confirm3':
                    bot.send_message(user_id, 'Подписка на 1 месяц, за 1199₽\n\n'
                                              'Вам необходимо отправить 1199₽ по номеру карты - \n\n'
                                              'После перевода вам необходимо отправить сообщение с вашими ФИО, мы проверим информацию и выдадим подписку!')
                    temp_user_data.temp_data(user_id)[user_id][0] = 12
                elif call.data == 'accept':
                    bot.send_message(chat_id=db_actions.get_user_id_from_topic(call.message.reply_to_message.id),
                                     text='Оплата принята!\n\n'
                                          'Можете пользоваться ботом!')
                elif call.data == 'deny':
                    bot.send_message(db_actions.get_user_id_from_topic(call.message.reply_to_message.id),
                                     'Оплата не принята! Попробуйте еще раз!')
                else:
                    bot.send_message(user_id, 'У вас закончилась пробная подписка!\n',
                                     reply_markup=buttons.buy_subscribe())
        else:
            bot.send_message(user_id, 'Введите /start для запуска бота')

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, config.get_config()['xlsx_path'])
    threading.Thread(target=schedule_check, args=()).start()
    schedule.every().second.do(func)
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    admin_ids = config.get_config()['admins']
    main()

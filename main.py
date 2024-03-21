#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
config_name = 'secrets.json'
#####################################
import os
import telebot
import platform
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import TempUserData, DbAct
from db import DB


def is_admin(user_id, admin_ids):
    return user_id in admin_ids

def main():
    @bot.message_handler(commands=['start', 'admin'])
    def start_message(message):
        name_user = message.from_user.first_name
        user_id = message.from_user.id
        command = message.text.replace('/', '')
        buttons = Bot_inline_btns()
        if command == 'start':
            bot.send_message(message.chat.id,
                             f'Привет, {name_user}! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                             reply_markup=buttons.start_btns())
        elif is_admin(user_id, admin_ids):
            if command == 'admin':
                bot.send_message(message.chat.id,
                                 f'Привет, {name_user}!',
                                 reply_markup=buttons.admin_btns())

    @bot.message_handler(content_types=['text', 'photo'])
    def text(message):
        user_id = message.chat.id
        code = temp_user_data.temp_data(user_id)[user_id][0]
        if code == 0:
            bot.send_message(message.chat.id, 'Выберите категорию!')
            temp_user_data.temp_data(user_id)[user_id][0] = 1
        elif code == 1:
            bot.send_message(message.chat.id, 'Название добавлено!')
            bot.send_message(message.chat.id, 'Отправьте рецепт! (одим сообщением)')
            temp_user_data.temp_data(user_id)[user_id][0] = 2
        elif code == 2:
            bot.send_message(message.chat.id, 'Данные сохранены')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user = call.message.from_user.id
        button_text = call.message.text
        user_id = call.message.chat.id
        buttons = Bot_inline_btns()
        if call.data == "go":
            bot.send_message(call.message.chat.id,
                             'Какой возраст у твоего ребенка?',
                             reply_markup=buttons.age_btns())
        elif call.data == "seven_months" or call.data == "eight_months" or call.data == "nine_months" or call.data == "ten_months" or call.data == "eleven_months" or call.data == "one_and_more":
            bot.send_message(call.message.chat.id,
                             'Отлично! Теперь ты можешь выбрать прием пищи, и я отправлю рецепт в зависимости от возраста ребенка!',
                             reply_markup=buttons.meal_btns())
        elif call.data == 'breakfast':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'garnir':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'soups':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'meat':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'fish':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'snack':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'nextrecipe':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'mainmenu':
            bot.send_message(call.message.chat.id,
                             f'Привет! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                             reply_markup=buttons.start_btns())
        elif call.data == 'newrecept':
            bot.send_message(call.message.chat.id, 'Выберите для какого возраста!', reply_markup=buttons.new_recept())
            # должна добавляться в бд инфа о кнопке нажатой и ожидать когда пользователь нажмет на кнопку
            bot.send_message(call.message.chat.id, 'Выберите категорию!', reply_markup=buttons.new_recept2())
            # так же добавляется инфа о нажатой кнопки, чтобы потом эту инфу выдать пользователю
            # и потом по tempuserdate добавить инфу о названии еды, фотку еды и сам рецепт
    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config)
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    admin_ids = config.get_config()['admins']
    main()

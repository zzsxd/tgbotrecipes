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
from config_parser import ConfigParser
from frontend import Bot_inline_btns


def main():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        name_user = message.from_user.first_name
        buttons = Bot_inline_btns()
        bot.send_message(message.chat.id,
                         f'Привет, {name_user}! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                         reply_markup=buttons.start_btns())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        name_user = call.message.from_user.first_name
        buttons = Bot_inline_btns()
        if call.data == "go":
            bot.send_message(call.message.chat.id,
                             'Какой возраст у твоего ребенка?',
                             reply_markup=buttons.age_btns())
        elif call.data == "seven_months" or call.data == "eight_months" or call.data == "nine_months" or call.data == "ten_months" or call.data == "eleven_months" or call.data == "one_and_more":
            bot.send_message(call.message.chat.id,
                             'Отлично! Теперь ты можешь выбрать прием пищи, и я отправлю рецепт в зависимости от возраста ребенка! ',
                             reply_markup=buttons.meal_btns())
        elif call.data == 'breakfast' or call.data == 'garnir' or call.data == 'soups' or call.data == 'meat' or call.data == 'fish' or call.data == 'snack':
            bot.send_message(call.message.chat.id,
                             'фотка, рецепт',
                             reply_markup=buttons.food_btns())
        elif call.data == 'nextrecipe':
            bot.send_message(call.message.chat.id, 'фотка, рецепт', reply_markup=buttons.food_btns())
        elif call.data == 'mainmenu':
            bot.send_message(call.message.chat.id,
                             f'Привет, {name_user}! Я Ковапу - твой помощник по кулинарии. Давай познакомимся!',
                             reply_markup=buttons.start_btns())
    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()

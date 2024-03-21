#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import telebot
from telebot import types

#####################################

class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_btns(self):
        go = types.InlineKeyboardButton('Давай!', callback_data="go")
        buy = types.InlineKeyboardButton('Подписка', callback_data="buy")
        self.__markup.add(go, buy)
        return self.__markup

    def age_btns(self):
        seven = types.InlineKeyboardButton('7 месяцев', callback_data="seven_months")
        eight = types.InlineKeyboardButton('8 месяцев', callback_data="eight_months")
        nine = types.InlineKeyboardButton('9 месяцев', callback_data="nine_months")
        ten = types.InlineKeyboardButton('10 месяцев', callback_data="ten_months")
        eleven = types.InlineKeyboardButton('11 месяцев', callback_data="eleven_months")
        one_and_more = types.InlineKeyboardButton('1 годик и старше', callback_data="one_and_more")
        self.__markup.add(seven, eight, nine, ten, eleven, one_and_more)
        return self.__markup

    def meal_btns(self):
        breakfast = types.InlineKeyboardButton('Завтрак', callback_data="breakfast")
        garnish = types.InlineKeyboardButton('Гарнир', callback_data="garnir")
        soups = types.InlineKeyboardButton('Супы', callback_data="soups")
        meat = types.InlineKeyboardButton('Мясо', callback_data="meat")
        fish = types.InlineKeyboardButton('Рыба', callback_data='fish')
        snack = types.InlineKeyboardButton('Перекус', callback_data='snack')
        self.__markup.add(breakfast, garnish, soups, meat, fish, snack)
        return self.__markup

    def food_btns(self):
        next_recipe = types.InlineKeyboardButton('Следующий рецепт', callback_data='nextrecipe')
        main_menu = types.InlineKeyboardButton('Главное меню', callback_data='mainmenu')
        self.__markup.add(next_recipe, main_menu)
        return self.__markup

    def admin_btns(self):
        new_recept = types.InlineKeyboardButton('Создать рецепт', callback_data='newrecept')
        self.__markup.add(new_recept)
        return self.__markup

    def new_recept(self):
        seven = types.InlineKeyboardButton('7 месяцев', callback_data="seven")
        eight = types.InlineKeyboardButton('8 месяцев', callback_data="eight")
        nine = types.InlineKeyboardButton('9 месяцев', callback_data="nine")
        ten = types.InlineKeyboardButton('10 месяцев', callback_data="ten")
        eleven = types.InlineKeyboardButton('11 месяцев', callback_data="eleven")
        one_and_more = types.InlineKeyboardButton('1 годик и старше', callback_data="one")
        self.__markup.add(seven, eight, nine, ten, eleven, one_and_more)
        return self.__markup

    def new_recept2(self):
        breakfast = types.InlineKeyboardButton('Завтрак', callback_data="breakfast1")
        garnish = types.InlineKeyboardButton('Гарнир', callback_data="garnir2")
        soups = types.InlineKeyboardButton('Супы', callback_data="soups3")
        meat = types.InlineKeyboardButton('Мясо', callback_data="meat4")
        fish = types.InlineKeyboardButton('Рыба', callback_data='fish5')
        snack = types.InlineKeyboardButton('Перекус', callback_data='snack6')
        self.__markup.add(breakfast, garnish, soups, meat, fish, snack)
        return self.__markup
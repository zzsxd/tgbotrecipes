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
        seven = types.InlineKeyboardButton('7 месяцев', callback_data="get7")
        eight = types.InlineKeyboardButton('8 месяцев', callback_data="get8")
        nine = types.InlineKeyboardButton('9 месяцев', callback_data="get9")
        ten = types.InlineKeyboardButton('10 месяцев', callback_data="get10")
        eleven = types.InlineKeyboardButton('11 месяцев', callback_data="get11")
        one_and_more = types.InlineKeyboardButton('1 годик и старше', callback_data="get+")
        self.__markup.add(seven, eight, nine, ten, eleven, one_and_more)
        return self.__markup

    def meal_btns(self):
        breakfast = types.InlineKeyboardButton('Завтрак', callback_data="kal1")
        garnish = types.InlineKeyboardButton('Гарнир', callback_data="kal2")
        soups = types.InlineKeyboardButton('Супы', callback_data="kal3")
        meat = types.InlineKeyboardButton('Мясо', callback_data="kal4")
        fish = types.InlineKeyboardButton('Рыба', callback_data='kal5')
        snack = types.InlineKeyboardButton('Перекус', callback_data='kal6')
        self.__markup.add(breakfast, garnish, soups, meat, fish, snack)
        return self.__markup

    def food_btns(self):
        next_recipe = types.InlineKeyboardButton('Следующий рецепт', callback_data='nextrecipe')
        main_menu = types.InlineKeyboardButton('Главное меню', callback_data='mainmenu')
        self.__markup.add(next_recipe, main_menu)
        return self.__markup

    def back_btn(self):
        main_menu = types.InlineKeyboardButton('Главное меню', callback_data='mainmenu')
        self.__markup.add(main_menu)
        return self.__markup

    def admin_btns(self):
        new_recept = types.InlineKeyboardButton('Создать рецепт', callback_data='newrecept')
        export = types.InlineKeyboardButton('Экспорт БД', callback_data='export')
        newsletter = types.InlineKeyboardButton('Создать рассылку', callback_data='newsletter')
        self.__markup.add(new_recept, export, newsletter)
        return self.__markup

    def new_recept(self):
        seven = types.InlineKeyboardButton('7 месяцев', callback_data="recept7")
        eight = types.InlineKeyboardButton('8 месяцев', callback_data="recept8")
        nine = types.InlineKeyboardButton('9 месяцев', callback_data="recept9")
        ten = types.InlineKeyboardButton('10 месяцев', callback_data="recept10")
        eleven = types.InlineKeyboardButton('11 месяцев', callback_data="recept11")
        one_and_more = types.InlineKeyboardButton('1 годик и старше', callback_data="recept+")
        self.__markup.add(seven, eight, nine, ten, eleven, one_and_more)
        return self.__markup

    def new_recept2(self):
        breakfast = types.InlineKeyboardButton('Завтрак', callback_data="govno1")
        garnish = types.InlineKeyboardButton('Гарнир', callback_data="govno2")
        soups = types.InlineKeyboardButton('Супы', callback_data="govno3")
        meat = types.InlineKeyboardButton('Мясо', callback_data="govno4")
        fish = types.InlineKeyboardButton('Рыба', callback_data='govno5')
        snack = types.InlineKeyboardButton('Перекус', callback_data='govno6')
        self.__markup.add(breakfast, garnish, soups, meat, fish, snack)
        return self.__markup
    def buy_subscribe(self):
        month = types.InlineKeyboardButton('Месяц - 299₽', callback_data="month")
        threemonth = types.InlineKeyboardButton('3 месяца - 599₽', callback_data='3month')
        year = types.InlineKeyboardButton('Год - 1199₽', callback_data='year')
        self.__markup.add(month, threemonth, year)
        return self.__markup

    def confirm_data_month(self):
        yes = types.InlineKeyboardButton('Подтверждаю', callback_data='confirm1')
        cancel = types.InlineKeyboardButton('Отмена', callback_data='mainmenu')
        self.__markup.add(yes, cancel)
        return self.__markup
    def confirm_data_3month(self):
        yes = types.InlineKeyboardButton('Подтверждаю', callback_data='confirm2')
        cancel = types.InlineKeyboardButton('Отмена', callback_data='mainmenu')
        self.__markup.add(yes, cancel)
        return self.__markup
    def confirm_data_year(self):
        yes = types.InlineKeyboardButton('Подтверждаю', callback_data='confirm3')
        cancel = types.InlineKeyboardButton('Отмена', callback_data='mainmenu')
        self.__markup.add(yes, cancel)
        return self.__markup

    def manager_btns(self):
        accept = types.InlineKeyboardButton('Подтвердить!', callback_data='accept')
        deny = types.InlineKeyboardButton('Отклонить!', callback_data='deny')
        self.__markup.add(accept, deny)
        return self.__markup
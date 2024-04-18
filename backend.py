#####################################
#            Created by             #
#               zzsxd               #
#####################################
import os
from datetime import datetime, timedelta
import time
import requests
import schedule
from openpyxl import load_workbook
import pandas as pd
#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: [None, None, None, [None, None, None, None, None], None, None]})
        return self.__user_data


class DbAct:
    def __init__(self, db, config, path_xlsx):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config
        self.__fields = {0: "Имя", 1: 'Фамилия', 2: 'Никнейм'}

    def add_user(self, user_id, first_name, last_name, nick_name):
        if not self.user_is_existed(user_id):
            if user_id in self.__config.get_config()['admins']:
                is_admin = True
            else:
                is_admin = False
            self.__db.db_write('INSERT INTO users (user_id, first_name, last_name, nick_name, is_admin, expiration_date) VALUES (?, ?, ?, ?, ?, ?)', (user_id, first_name, last_name, nick_name, is_admin, int(time.time()+259200)))

    def user_is_existed(self, user_id):
        data = self.__db.db_read('SELECT count(*) FROM users WHERE user_id = ?', (user_id, ))
        if len(data) > 0:
            if data[0][0] > 0:
                status = True
            else:
                status = False
            return status

    def user_is_admin(self, user_id):
        data = self.__db.db_read('SELECT is_admin FROM users WHERE user_id = ?', (user_id, ))
        if len(data) > 0:
            if data[0][0] == 1:
                status = True
            else:
                status = False
            return status

    def update_fisting(self, state, tg_nick):
        match state:
            case '1':
                new_fisting = time.time() + 2629746
            case '2':
                new_fisting = time.time() + 2629746*3
            case '3':
                new_fisting = time.time() + 2629746*12
        self.__db.db_write('UPDATE users SET expiration_date = ?, endsubscribe = ? WHERE nick_name = ?', (int(new_fisting), False, tg_nick))

    def add_recept(self, data):
        self.__db.db_write('INSERT INTO recipes (age, category, photo, title, recipe) VALUES (?, ?, ?, ?, ?)', data)

    def get_exp_date(self, user_id):
        return int(self.__db.db_read('SELECT expiration_date FROM users WHERE user_id = ?', (user_id, ))[0][0])

    def get_recepts(self, age, category):
        return self.__db.db_read('SELECT photo, title, recipe FROM recipes WHERE age = ? AND category = ?', (age, category))

    def check_subscribe(self):
        return self.__db.db_read("SELECT user_id, expiration_date FROM users WHERE is_admin = 0", ())

    def get_user_id(self):
        return self.__db.db_read("SELECT user_id FROM users", ())

    def ban_user(self, user_id):
        check = self.__db.db_read("SELECT endsubscribe FROM users WHERE user_id = ?", (user_id,))[0][0]
        if check is None or check == 0:
            self.__db.db_write("UPDATE users SET endsubscribe = ? WHERE user_id = ?", (True, user_id))

    def have_ban(self, user_id):
        is_ban = self.__db.db_read("SELECT endsubscribe FROM users WHERE user_id=?", (user_id,))[0][0]
        if is_ban == 1:
            return True
        else:
            return False

    def db_export_xlsx(self):
        d = {'Имя': [], 'Фамилия': [], 'Никнейм': []}
        users = self.__db.db_read('SELECT first_name, last_name, nick_name FROM users', ())
        if len(users) > 0:
            for user in users:
                for info in range(len(list(user))):
                    d[self.__fields[info]].append(user[info])
            df = pd.DataFrame(d)
            df.to_excel(self.__config.get_config()['xlsx_path'], sheet_name='пользователи', index=False)
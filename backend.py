#####################################
#            Created by             #
#               zzsxd               #
#####################################
import os
import time
import requests
from datetime import datetime, timedelta
#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: [None, None, None, [None, None, None, None, None], None]})
        return self.__user_data


class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config

    def add_user(self, user_id, first_name, last_name, nick_name):
        if not self.user_is_existed(user_id):
            if user_id in self.__config.get_config()['admins']:
                is_admin = True
            else:
                is_admin = False
            self.__db.db_write('INSERT INTO users (user_id, first_name, last_name, nick_name, is_admin) VALUES (?, ?, ?, ?, ?)', (user_id, first_name, last_name, nick_name, is_admin))

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

    def add_recept(self, data):
        self.__db.db_write('INSERT INTO recipes (age, category, photo, title, recipe) VALUES (?, ?, ?, ?, ?)', data)

    def get_recepts(self, age, category):
        return self.__db.db_read('SELECT photo, title, recipe FROM recipes WHERE age = ? AND category = ?', (age, category))

    def give_free_subscribe(self, expiration_date):
        expiration_date = datetime.now() + timedelta(days=3)
        return self.__db.db_write("INSERT OR REPLACE INTO subscriptions (expiration_date) VALUES (?)", (expiration_date))

    def check_subscribe(self, user_id, expiration_date):
        return self.__db.db_read("SELECT expiration_date FROM users WHERE user_id=?", (user_id,))

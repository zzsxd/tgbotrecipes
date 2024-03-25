#####################################
#            Created by             #
#               zzsxd               #
#####################################
import os
import sqlite3


#####################################

class DB:
    def __init__(self, path, lock):
        super(DB, self).__init__()
        self.__lock = lock
        self.__db_path = path
        self.__cursor = None
        self.__db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()
            self.__cursor.execute('''
                        CREATE TABLE users(
                        row_id INTEGER primary key autoincrement not null,
                        user_id INTEGER,
                        first_name TEXT,
                        last_name TEXT,
                        nick_name TEXT,
                        is_admin BOOL,
                        expiration_date TEXT,
                        UNIQUE(user_id)
                        )
                        ''')
            self.__cursor.execute('''
                CREATE TABLE recipes(
                row_id INTEGER PRIMARY KEY autoincrement not null, 
                age INTEGER, 
                category INTEGER, 
                photo BLOB, 
                title TEXT, 
                recipe TEXT)
                ''')
            self.__db.commit()
        else:
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()

    def db_write(self, queri, args):
        self.set_lock()
        self.__cursor.execute(queri, args)
        self.__db.commit()
        self.realise_lock()

    def db_read(self, queri, args):
        self.set_lock()
        self.__cursor.execute(queri, args)
        self.realise_lock()
        return self.__cursor.fetchall()

    def set_lock(self):
        self.__lock.acquire(True)

    def realise_lock(self):
        self.__lock.release()
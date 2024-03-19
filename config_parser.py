#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
import os
import sys


#####################################


class ConfigParser:
    def __init__(self, file_path, os_type):
        super(ConfigParser, self).__init__()
        self.__file_path = file_path
        self.__default_pathes = {'Windows': 'C:\\', 'Linux': '/'}
        self.__default = {'tg_api': '', 'admins': [], 'db_file_name': '', 'FAQ': '', 'contacts': '', 'start_msg': '', 'step_sale': 500, 'percent_sale': 0, 'terminal_key': '', 'terminal_password': '', 'token': ''}
        self.__current_config = None
        self.load_conf()

    def load_conf(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                self.__current_config = json.loads(file.read())
            if len(self.__current_config['tg_api']) == 0:
                sys.exit('config is invalid')
        else:
            self.create_conf(self.__default)
            sys.exit('config is not existed')

    def create_conf(self, config):
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(config, sort_keys=True, indent=4))

    def get_config(self):
        return self.__current_config

    def update_faq(self, new_path):
        self.__current_config['FAQ'] = new_path
        self.create_conf(self.__current_config)

    def update_contacts(self, new_path):
        self.__current_config['contacts'] = new_path
        self.create_conf(self.__current_config)

    def update_start_msg(self, new_path):
        self.__current_config['start_msg'] = new_path
        self.create_conf(self.__current_config)

    def change_contacts(self, new_path):
        self.__current_config['contacts'] = new_path
        self.create_conf(self.__current_config)

    def change_faq(self, new_path):
        self.__current_config['FAQ'] = new_path
        self.create_conf(self.__current_config)

    def change_start_msg(self, new_path):
        self.__current_config['start_msg'] = new_path
        self.create_conf(self.__current_config)

    def change_step(self, new_path):
        self.__current_config['step_sale'] = new_path
        self.create_conf(self.__current_config)

    def change_percent(self, new_path):
        self.__current_config['percent_sale'] = new_path
        self.create_conf(self.__current_config)

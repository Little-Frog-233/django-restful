import os
import sys
import configparser

current_path = os.path.realpath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
cfp = configparser.ConfigParser()
cfp.read(os.path.join(root_path, 'conf/web.conf'), encoding='utf-8')

class Config:
    def __init__(self):
        self.sql_host = cfp.get('mysql', 'host')
        self.sql_port = cfp.get('mysql', 'port')
        self.sql_database = cfp.get('mysql', 'database')
        self.sql_username = cfp.get('mysql', 'username')
        self.sql_password = cfp.get('mysql', 'password')

if __name__ == '__main__':
    print(root_path)
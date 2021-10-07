import sqlite3 as sql
import os.path
from config import CONFIG_DB


class DataBase:
    connection = None
    cur = None

    def __init__(self, path, is_exists=False):
        self.schema = CONFIG_DB['base_model']
        self.SQL_IR_QUERY = CONFIG_DB['tgm_insert_query']
        self.SQL_AI_QUERY = CONFIG_DB['tgm_after_insert_query']
        self.SQL_EX_QUERY = CONFIG_DB['tgm_export_query']
        if is_exists:
            self.db_connect(path)
        else:
            self.db_init(path)

    def db_init(self, path):
        with open(self.schema, 'r') as sql_file:
            sql_script = sql_file.read()

        if os.path.exists(path):
            os.remove(path)
        self.connection = sql.connect(path)
        self.cur = self.connection.cursor()
        self.cur.executescript(sql_script)
        self.connection.commit()

    def db_connect(self, path):
        self.connection = sql.connect(path)
        self.cur = self.connection.cursor()

    def db_close(self):
        self.connection.close()

    def db_save_tg_message_data(self, data):
        self.cur.executemany(self.SQL_IR_QUERY, [tuple(i.values()) for i in data])
        self.cur.execute(self.SQL_AI_QUERY)
        self.connection.commit()

    def db_export_txt_tg_message_data(self, path):
        self.cur.execute(self.SQL_EX_QUERY)
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'w', encoding='utf8') as outfile:
            outfile.writelines([row[0] for row in self.cur.fetchall()])

#-*- coding:utf-8 -*-
import psycopg2

class DataBase:
    def __init__(self, db_name, password):
        self.conn = psycopg2.connect(database=db_name, user='public_wifi', password=password, host='localhost', port='5432')
        self.db_name = db_name
        self.conn.autocommit = True

    def dropTable(self):
        with self.conn.cursor() as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS {self.db_name};')

    def createTable(self):
        with self.conn.cursor() as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.db_name} (ap_no INTEGER PRIMARY KEY, cities_and_provinces VARCHAR(20), city VARCHAR(20), detail_address TEXT, raw_detail_address TEXT, ap_name TEXT, latitude TEXT, longtitude TEXT);')

    def insertTable(self, ap_no, cities_and_provinces, city, detail_address, raw_detail_address, ap_name, latitude, longtitude):
        with self.conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO {self.db_name} VALUES ('{ap_no}', '{cities_and_provinces}', '{city}', '{detail_address}', '{raw_detail_address}', '{ap_name}', '{latitude}', '{longtitude}');")

    def search(self, search_word, MAX_RESULT):
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT raw_detail_address FROM {self.db_name} WHERE raw_detail_address ~* '{'|'.join(search_word.split())}';")
            return [i[0] for i in cursor.fetchall()]

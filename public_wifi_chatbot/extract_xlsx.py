#-*- coding:utf-8 -*-
from openpyxl import load_workbook
from .database import DataBase
import json

load_wb = load_workbook('public_wifi.xlsx', data_only=True)

load_ws = load_wb['ap위치정보']

# unique_num_col | cities_and_provinces_col | city_col | detail_address_col | ap_name_col | latitude_col | longtitude_col

with open('db_pw.json', 'rt', encoding='utf-8') as f:
    pw = json.loads(f.read())['password']

db = DataBase('public_wifi', pw)

db.dropTable()

db.createTable()

for row in load_ws.rows:
    r = []
    for i in row:
        r.append(i.value)
    if ('ROOT' in r) or (None in r) or (r[0] == '번호'):
        continue
    unique_num, cities_and_provinces, city, detail_address, ap_name, latitude, longtitude = r
    db.insertTable(unique_num, cities_and_provinces, city, detail_address, f'{cities_and_provinces} {city} {detail_address}', ap_name, latitude, longtitude)
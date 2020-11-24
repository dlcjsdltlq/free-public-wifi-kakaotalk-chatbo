#-*- coding:utf-8 -*-
from database import DataBase
import json

class SearchAddress:
    def __init__(self):
        with open('db_pw.json', 'rt', encoding='utf-8') as f:
            self.pw = json.loads(f.read())['password']
            self.db = DataBase('public_wifi', self.pw)

    def hasString(self, str1, str_list):
        for str in str_list:
            if not str in str1:
                return False
        return True

    def search(self, search_keyword):
        search_datas = self.db.search(search_keyword, 100)
        result = []
        for search_data in search_datas:
            if self.hasString(search_data, search_keyword.split()):
                result.append(' '.join(search_data.split()[2:]))
        return list(set(result))

if __name__ == '__main__':
    search_address = SearchAddress()
    query = input('검색할 지역을 입력해 주세요 > ')
    ss = search_address.search(query)
    if ss == []:
        print('검색결과가 없습니다!')
    for i in ss:
        print(i)
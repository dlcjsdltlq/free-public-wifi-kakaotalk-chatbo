#-*- coding:utf-8 -*-
from flask import Flask, request
from flask.json import jsonify
from search_address import SearchAddress
import threading
import atexit
import time

user_list = {}
POOL_TIME = 3
data_lock = threading.Lock()
user_manage_thread = threading.Thread()

search_address = SearchAddress()

def createApp():
    app = Flask(__name__)

    def interrupt():
        global user_manage_thread
        user_manage_thread.cancel()

    def manageUserList():
        global user_list, user_manage_thread, data_lock
        with data_lock:
            try:
                for user_id in user_list:
                    cur_time = user_list[user_id][1]
                    if time.time() - cur_time > 600:
                        del user_list[user_id]
            except: pass
        user_manage_thread = threading.Timer(POOL_TIME, manageUserList, ())
        user_manage_thread.start()

    def manageUserListStart():
        global user_manage_thread
        user_manage_thread = threading.Timer(POOL_TIME, manageUserList, ())
        user_manage_thread.start()

    manageUserListStart()
    atexit.register(interrupt)
    return app

app = createApp()

@app.route('/')
def index():
    return '<h1>공공와이파이 카카오톡 챗봇 API 서버입니다.</h1>'

@app.route('/query', methods = ['POST'])
def query():
    global user_list
    recieved_data = request.get_json()
    response_data = {
        'version': '2.0',
        'template': {
            'outputs': [{
                    'simpleText': {
                        'text': ''
                    }
                }]
            }
        }
    msg = recieved_data['userRequest']['utterance'].strip()
    user_id = recieved_data['userRequest']['user']['id']
    resp = '명령을 입력해 주십시오.'
    if ('주소찾기' in msg) or ('주소 찾기' in msg):
        user_list[user_id] = ['F', time.time(), []]
        resp = '주소를 입력해 주세요.'

    elif (user_id in user_list) and (user_list[user_id][0] == 'N') and (msg.upper() == 'Q'):
        del user_list[user_id]
        resp = '검색을 종료합니다.'

    elif (user_id in user_list) and (user_list[user_id][0] == 'N')  and (msg.upper() == 'N'):
        if len(user_list[user_id][2]) > 0:
            resp = user_list[user_id][2].pop(0)
        else:
            resp = '검색이 끝났습니다.'
            del user_list[user_id]

    elif (user_id in user_list) and (user_list[user_id][0] == 'F'):
        result = []
        try: result = search_address.search(msg)
        except: pass
        msg = ''; q_idx = 1; msg_queue = []
        if not result: resp = '검색결과가 없습니다.'
        else:
            msg += f'총 {len(result)}개의 결과가 검색되었습니다.\n'
            if len(result) > 100:
                msg += '100개 초과일 경우 100건마다 나뉘어 검색됩니다.\n'
                msg += '다음 검색결과를 보시려면 n, 그만하시려면 q를 입력하세요.\n'
            for address in result:
                msg += f'{q_idx}. {address}\n'
                if q_idx == 100:
                    msg_queue.append(msg)
                    msg = ''; q_idx = 0
                q_idx += 1
            msg_queue.append(msg)
            msg_queue[-1] += '마지막 검색결과입니다.\n'
            resp = msg_queue.pop(0)
            if not user_id in user_list: user_list[user_id] = ['N', time.time(), []]
            user_list[user_id][0] = 'N'
            user_list[user_id][2] = msg_queue
    response_data['template']['outputs'][0]['simpleText']['text'] = resp
    return jsonify(response_data)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 各種設定項目 ##################################################
BASE_URL = 'https://api.twitch.tv/kraken/chat/{0}/rooms'

# モジュール読み込み #############################################
import urllib.request, urllib.parse # urlエンコードや，送信など
import re                           # 検索，置換など
import sys                          # system周りの制御用（exit）
import os                           # ファイルパス取得

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import requests
import json




# config file loading ########################################
config = {"Twitch_Channel":"", "Twitch_Username":"", "Twitch_TextColor":"",
            "Default_Language":"", "Default_TransLanguage":"",
            "Show_ByName":"", "Show_ByLang":"",
            "Sound":"",
            "channelID":"", "roomUUID":"",
            "Google_API_KEY":"", "Twitch_OAUTH":"", "say":"", "gTTS":""}

readfile = 'config.txt'
f = open(readfile, 'r')
lines = f.readlines()

cnt = 1
for l in lines:
    if l.find("#") == 0 or l.strip() == "":
        continue
    
    conf_line = l.split('=')
    if conf_line[0].strip() in config.keys():
        config[conf_line[0].strip()] = conf_line[1].strip()        

    cnt = cnt+1

f.close()

# twitch API への GET/POST リクエスト時のヘッダ情報 #########
headers = {'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': 'q6batx0epp608isickayubi39itsckt',
            'Authorization': 'OAuth {}'.format(config["Twitch_OAUTH"]).replace('oauth:','')}

# 接続先の USER ID をゲット ################################
print(config['Twitch_Channel'].lstrip('#'))
getid = requests.get('https://api.twitch.tv/kraken/users?login={}'.format(config['Twitch_Channel'].lstrip('#')), headers=headers)

getid_json = json.loads(getid.text)
USER_ID = getid_json['users'][0]['_id']

# 接続URLなど準備 ###############################################
url     = BASE_URL.format(USER_ID)

# APIに接続 ##############################################
try:
    res = requests.get(url, headers=headers)
except Exception as e:
    print("例外args:", e.args)
    print("エラー：対話APIに接続できません")

print('\n############### CHAT ROOM INFORMATION ###############')
print('CHANNEL NAME : {} ({})'.format(getid_json['users'][0]['display_name'], getid_json['users'][0]['name']))
print('')

chat_info = json.loads(res.text)
for i,room in enumerate(chat_info['rooms']):
    print('--- Room No.{:>2} [NAME: {}] ---'.format(i, room['name']))
    for d in room.keys():
        print(' {:<10}: {}'.format(d, room[d]))
    print('')




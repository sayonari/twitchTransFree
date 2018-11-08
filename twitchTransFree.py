#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Title       : Automatic Translator for Twitch Chat
Developer   : husband_sayonari_omega
github      : http://github.com/sayonari/twitchTrans
mail        : sayonari@gmail.com
'''

# import modules ###########################################
# for IRC -------------
import sys, socket, os

# for POST query -----
import requests
import re

# for say ------------
import subprocess

# for Google TTS & play --------
from gtts import gTTS
from playsound import playsound
import shutil
import time

# configurte for Google TTS & play
TMP_DIR = './tmp/'
tts_cnt = 0

# 作業用ディレクトリ削除 ＆ 作成
if os.path.exists(TMP_DIR):
    du = shutil.rmtree(TMP_DIR)
    time.sleep(0.3)

os.mkdir(TMP_DIR)

# for Unicode charactor check
import unicodedata

# configure #################################################
DEBUG = False
TARGET = "irc.twitch.tv"
PORT = 6667
BUF_SIZE = 1024

url = 'https://translate.google.com/'

config = {"Twitch_Channel":"", "Twitch_Username":"", "Twitch_TextColor":"",
            "Default_Language":"", "Default_TransLanguage":"",
            "Show_ByName":"", "Show_ByLang":"",
            "NOT_SendToChat":"", "Sound":"",
            "channelID":"", "roomUUID":"",
            "Google_API_KEY":"", "Twitch_OAUTH":"", "say":"", "gTTS":""}

# config file loading ########################################
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
    else:
        print("ERROR: " + conf_line[0].strip() + " is can't use in config.txt [line " + str(cnt) + "]! please check it.")
        exit()
    cnt = cnt+1

f.close()

# fix some config bugs ##########

# miss "#" mark ------
if not config["Twitch_Channel"].startswith('#'):
    print("miss # mark! I add '#' to 'config:Twitch_Channel'")
    config["Twitch_Channel"] = "#" + config["Twitch_Channel"]


print(config["Twitch_Channel"])


# initialize #################################################
TargetLangs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW", "co",
                "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha",
                "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky",
                "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa",
                "pl", "pt", "ma", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw",
                "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]

Voice = {"en":"Samantha", "it":"Alice", "sv":"Alva", "fr":"Amelie", "de":"Anna", "id":"Damayanti", "es":"Diego", "nl":"Ellen",
         "ro":"Ioana", "pt":"Joana", "th":"Kanya", "ja":"Kyoko", "sk":"Laura", "hi":"Lekha", "it":"Luca", "pt":"Luciana", 
         "ar":"Maged", "hu":"Mariska", "zh-TW":"Mei-Jia", "el":"Melina", "ru":"Milena", "nb":"Nora", "da":"Sara", "fi":"Satu", 
         "zh-CN":"Ting-Ting", "tr":"Yelda", "ko":"Yuna", "pl":"Zosia", "cs":"Zuzana"}

gTTS_Voice = {
    'af' : 'Afrikaans',
    'sq' : 'Albanian',
    'ar' : 'Arabic',
    'hy' : 'Armenian',
    'bn' : 'Bengali',
    'ca' : 'Catalan',
    'zh' : 'Chinese',
    'zh-cn' : 'Chinese (Mandarin/China)',
    'zh-tw' : 'Chinese (Mandarin/Taiwan)',
    'zh-yue' : 'Chinese (Cantonese)',
    'hr' : 'Croatian',
    'cs' : 'Czech',
    'da' : 'Danish',
    'nl' : 'Dutch',
    'en' : 'English',
    'en-au' : 'English (Australia)',
    'en-uk' : 'English (United Kingdom)',
    'en-us' : 'English (United States)',
    'eo' : 'Esperanto',
    'fi' : 'Finnish',
    'fr' : 'French',
    'de' : 'German',
    'el' : 'Greek',
    'hi' : 'Hindi',
    'hu' : 'Hungarian',
    'is' : 'Icelandic',
    'id' : 'Indonesian',
    'it' : 'Italian',
    'ja' : 'Japanese',
    'km' : 'Khmer (Cambodian)',
    'ko' : 'Korean',
    'la' : 'Latin',
    'lv' : 'Latvian',
    'mk' : 'Macedonian',
    'no' : 'Norwegian',
    'pl' : 'Polish',
    'pt' : 'Portuguese',
    'ro' : 'Romanian',
    'ru' : 'Russian',
    'sr' : 'Serbian',
    'si' : 'Sinhala',
    'sk' : 'Slovak',
    'es' : 'Spanish',
    'es-es' : 'Spanish (Spain)',
    'es-us' : 'Spanish (United States)',
    'sw' : 'Swahili',
    'sv' : 'Swedish',
    'ta' : 'Tamil',
    'th' : 'Thai',
    'tr' : 'Turkish',
    'uk' : 'Ukrainian',
    'vi' : 'Vietnamese',
    'cy' : 'Welsh'
}

received = ""

########################################################
# IRC functions ########################################
########################################################

# irc_connect ##########################################
def irc_connect(irc_socket, target, port):
    irc_socket.connect((target, port))

# login ##########################################
def login(irc_server, nickname, username, realname, hostname = "hostname", servername = "*"):
    pass_message = "PASS " + config["Twitch_OAUTH"] + "\n"
    nick_message = "NICK " + nickname + "\n"
    user_message = "USER %s %s %s :%s\n" % (username, hostname, servername, realname)

    irc_server.send(bytes(pass_message,"UTF-8"))
    irc_server.send(bytes(nick_message,"UTF-8"))
    irc_server.send(bytes(user_message,"UTF-8"))

# join ##########################################
def join(irc_server, channel):
    join_message = "JOIN " + channel + "\n"
    print(join_message)

    irc_server.send(bytes(join_message,"UTF-8"))

# pong ##########################################
def pong(irc_server, daemon, daemon2 = None):
    pong_message = "PONG %s %s" % (daemon, daemon2)
    pong_message += "\n"

    irc_server.send(bytes(pong_message,"UTF-8"))

# privmsg ##########################################
def privmsg(irc_server, channel, text):
    privmsg_message = "PRIVMSG %s :%s\n" % (channel, text)
    print(privmsg_message)

    irc_server.send(bytes(privmsg_message,"UTF-8"))

# quit ##########################################
def quit(irc_server):
    None

# handle_privmsg ##########################################
def handle_privmsg(irc_server, prefix, receiver, text):
     # twitch message ------------------
    twitch_msg = text
    twitch_username = prefix.split("!")[0]
 
    # text check -----------------------
    if DEBUG: print ("")
    print (twitch_username + "　>　" + twitch_msg)
    if DEBUG: print ("")

    # initialize ----------------------
    target_lang = config["Default_Language"]
    target_text = ""
    source_lang = ""
    source_text = ""

    all_line = ""
    all_line_noaps = ""

    # forbidden check -----------------
    if "http" in twitch_msg:
        return 0

    match = re.search('bot$', twitch_username)
    if match:
        return 0
    
    twitch_msg = re.sub(r'ACTION[\s ]*', "", twitch_msg) 

    # command execution ---------------
    if config["Sound"] == "True" and re.match('^\!sound ', twitch_msg):
        sound_name = twitch_msg.strip().split(" ")[1]
        if DEBUG: print("Play sound: ./sound/{}.mp3".format(sound_name))
        try:
            playsound('./sound/{}.mp3'.format(sound_name), True)
        except:
            print('エラー起こった at playsound')
            import traceback
            traceback.print_exc()
        return 0

    # target language -----------------
    match = re.match('(.{2,5}?):', twitch_msg)
    if match:
        target_lang = match.group(1)
        source_text = ''.join(twitch_msg.split(':')[1:])
    else:
        source_text = twitch_msg

    # jp > ja -------------------------
    if target_lang == "jp":
        target_lang = "ja"

    # detect source language & force JAPANESE trans -----------
    if target_lang in TargetLangs:
        params = {
            "q": source_text,
            "tl": target_lang,
            "sl": "auto"
        }
        r = requests.get(url=url, params=params)
        source_lang = re.search("sl=(.*?)[&\"]", r.text).group(1)
        if re.search("TRANSLATED_TEXT=\'(.*?)\'", r.text):
            target_text = re.search("TRANSLATED_TEXT=\'(.*?)\'", r.text).group(1)
        else:
            target_text = ""

    # source = target = "ja"
    if source_lang == config["Default_Language"] and target_lang == config["Default_Language"]:
        target_lang = config["Default_TransLanguage"]
        params = {
            "q": source_text,
            "sl": source_lang,
            "tl": target_lang
        }
        r = requests.get(url=url, params=params)
        source_lang = re.search("sl=(.*?)[&\"]", r.text).group(1)
        if re.search("TRANSLATED_TEXT=\'(.*?)\'", r.text):
            target_text = re.search("TRANSLATED_TEXT=\'(.*?)\'", r.text).group(1)
        else:
            target_text = ""

    # print&tts trans text --------
    all_line = conv(html_decode(target_text))
    print(all_line + "\n")

    line_send = "/me "  + str(all_line)
    if config["Show_ByName"]=="True": line_send += " [by_" + str(twitch_username) + "]"
    if config["Show_ByLang"]=="True": line_send += " (" + source_lang + ")"

    # TransRoomName が設定されてたら，そこに投稿する
    # NOT_SendToChat が'False'だったら送信する
    if not config["NOT_SendToChat"]=="True":
        if config["channelID"]:
            print('put to ...')
            privmsg(irc_server, '{}:{}:{}'.format("#chatrooms", config["channelID"], config["roomUUID"]), line_send)
        else:
            if DEBUG :
                print('TransRoomName: none')
            privmsg(irc_server, config["Twitch_Channel"], line_send)

    # 音声合成出力 ----------------------------------
    if config["say"] == "True" or config["gTTS"] == "True":
        source_text = unicodedata.normalize('NFKC', source_text)
        source_text = re.sub(r'[︰-＠]', " ", source_text) 
        source_text = re.sub(r'[!-/]', " ", source_text)
        source_text = re.sub(r'[:-@]', " ", source_text)
        all_line_noaps = unicodedata.normalize('NFKC', all_line_noaps)
        all_line_noaps = re.sub(r'[︰-＠]', " ", all_line)         # Zenkaku kigou
        all_line_noaps = re.sub(r'[!-/]', " ", all_line_noaps)    # Hankaku Kigou
        all_line_noaps = re.sub(r'[:-@]', " ", all_line_noaps)    # Hankaku Kigou

        source_text = re.sub(r'^[¥s　]+$', "", source_text)
        all_line_noaps = re.sub(r'^[¥s　]+$', "", all_line_noaps)

        source_text = source_text.strip()
        all_line_noaps = all_line_noaps.strip()

        if source_text:
            if DEBUG: print("[DEBUG] source_lang:" + source_lang + " source_text:" + source_text)
            if config["say"] == "True":
                say(source_lang, source_text)
            
            if config["gTTS"] == "True":
                gTTS_play(source_lang, source_text)
                

        if target_lang and all_line_noaps:
            if DEBUG: print("[DEBUG] target_lang:" + target_lang + " target_text:" + target_text)
            if config["say"] == "True":
                say(target_lang, all_line_noaps)
            
            if config["gTTS"] == "True":
                gTTS_play(target_lang, all_line_noaps)




# wait_message ##########################################
def wait_message(irc_server):
    while(True):
        msg_buf_all = irc_server.recv(BUF_SIZE).decode("UTF-8")
        msg_buf_split = msg_buf_all.strip().splitlines()

        for msg_buf in msg_buf_split:
            # print("[DEBUG(msg)]")
            # print(msg_buf)

            prefix = None
            if msg_buf[0] == ":":
                p = msg_buf.find(" ")
                prefix = msg_buf[1:p]
                msg_buf = msg_buf[(p + 1):]

            p = msg_buf.find(":")
            if p != -1:#has last param which starts with ":"
                last_param = msg_buf[(p + 1):]
                msg_buf = msg_buf[:p]
                msg_buf = msg_buf.strip()

            messages = msg_buf.split()

            command = messages[0]
            params = messages[1:]

            if DEBUG:
                print("PARAMS:{}".format(params))

            if DEBUG:
                print("debug(message):",end="")
                print(messages)

            if command == "PING":
                pong(irc_server, "")
            elif command == "PRIVMSG":
                if params[0] == "#chatrooms":
                    continue

                else:
                    text = last_param
                    receiver = ""

                    for param in params:
                        receiver = param

                    handle_privmsg(irc_server, prefix, receiver, text)

# irc_main ##########################################
def irc_main():

    nickname = config["Twitch_Username"]
    username = config["Twitch_Username"]
    realname = config["Twitch_Username"]
    channel = config["Twitch_Channel"]

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_connect(irc, TARGET, PORT)
    login(irc, nickname, username, realname)

    join(irc, channel)
    privmsg(irc, channel, "/color " + config["Twitch_TextColor"])
    print("connect OK! : " + channel)

    # TransRoomName が設定されてたら，そこに投稿する
    if config["channelID"]:
        join(irc, '{}:{}:{}'.format("#chatrooms", config["channelID"], config["roomUUID"]))
        privmsg(irc, '{}:{}:{}'.format("#chatrooms", config["channelID"], config["roomUUID"]), "/color " + config["Twitch_TextColor"])
        print("connect OK! : " + channel)

    wait_message(irc)

        

# say: TTS ###################################################
def say(tl,text):
    if tl in Voice.keys():
        voice = Voice[tl]
    else:
        voice = Voice["ja"]

    subprocess.call('say -v ' + voice + ' ' + text, shell=True)

# gTTS_play: TTS ###################################################
def gTTS_play(tl,text):
    global TMP_DIR, tts_cnt, DEBUG
    if tl in gTTS_Voice.keys():
        voice = tl
    else:
        voice = "ja"
    
    tts = gTTS(text=text, lang=voice, slow=False)
    temp_tts = "{}/tmp_tts_{}.mp3".format(TMP_DIR, tts_cnt)
    tts.save(temp_tts)
    try:
        playsound(temp_tts, True)
    except:
        print('エラー起こった at playsound')
    os.remove(temp_tts)
    tts_cnt += 1

# 数値文字参照（10進数）のデコード ##############################
def conv(s):
    cs = s
    for e in re.findall("&#([0-9]+);", s):
        cs = cs.replace('&#{};'.format(e), chr(int(e, 10)))
    return cs

# html_decode ################################################
def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '\\x26#39;'),
            ('"', '\\x26quot;'),
            ('>', '\\x26gt;'),
            ('<', '\\x26lt;'),
            ('&', '\\x26amp;'),
            ('・', '&#183;'),
            ('ﾟ', '&#12442;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

##############################################################
# main #######################################################
##############################################################
if __name__ == "__main__":
    irc_main()
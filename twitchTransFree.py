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

# configure #################################################
TARGET = "irc.twitch.tv"
PORT = 6667
BUF_SIZE = 1024

url = 'https://translate.google.com/'

config = {"Twitch_Channel":"", "Twitch_Username":"", "Twitch_TextColor":"",
            "Default_Language":"", "Default_TransLanguage":"",
            "Google_API_KEY":"", "Twitch_OAUTH":""}

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

    irc_server.send(bytes(join_message,"UTF-8"))

# pong ##########################################
def pong(irc_server, daemon, daemon2 = None):
    pong_message = "PONG %s %s" % (daemon, daemon2)
    pong_message += "\n"

    irc_server.send(bytes(pong_message,"UTF-8"))

# privmsg ##########################################
def privmsg(irc_server, channel, text):
    privmsg_message = "PRIVMSG %s :%s\n" % (channel, text)

    irc_server.send(bytes(privmsg_message,"UTF-8"))

# quit ##########################################
def quit(irc_server):
    None

# handle_privmsg ##########################################
def handle_privmsg(irc_server, prefix, receiver, text):
    print ("")
    print (prefix.split('!')[0] + "　>　" + text)
    print ("")

    # initialize ----------------------
    target_lang = config["Default_Language"]
    target_text = ""
    source_lang = ""
    source_text = ""

    all_line = ""
    all_line_noaps = ""

    # twitch message ------------------
    twitch_msg = text
    twitch_username = prefix.split("!")[0]
    
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
        source_lang = re.search("sl=(.*?)&", r.text).group(1)
        target_text = re.search("TRANSLATED_TEXT=\'(.*?)\'", r.text).group(1)

    # source = target = "ja"
    if source_lang == config["Default_Language"] and target_lang == config["Default_Language"]:
        target_lang = config["Default_TransLanguage"]
        params = {
            "q": source_text,
            "sl": source_lang,
            "tl": target_lang
        }
        r = requests.get(url=url, params=params)
        source_lang = re.search("sl=(.*?)&", r.text).group(1)
        target_text = re.search("TRANSLATED_TEXT=\'(.*?)\'", r.text).group(1)

    # print&tts trans text --------
    all_line = target_text
    all_line = all_line.replace("&#39;","\'")

    line_send = "/me "  + str(all_line) + " [by_" + str(twitch_username) + "]"
    privmsg(irc_server, config["Twitch_Channel"], line_send)


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

            # print("debug(message):",end="")
            # print(messages)

            if command == "PING":
                pong(irc_server, "")
            elif command == "PRIVMSG":
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

    wait_message(irc)

        

# say: TTS ###################################################
def say(tl,text):
    if tl in Voice.keys():
        voice = Voice[tl]
    else:
        voice = Voice["ja"]

    subprocess.call('say -v' + voice + ' ' + text, shell=True)



##############################################################
# main #######################################################
##############################################################
if __name__ == "__main__":
    irc_main()
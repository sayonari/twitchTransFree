# Automatic Translator for Twitch Chat

## files ファイル
|file|explain|
|:-|:-|
|README.md               |This file                                 |
|config.txt              |text file for configulation               |
|twitchTransFree.py      |python program for Twitch Translate       |
|twitchTransFree_MacOS   |Binary for MacOS for Twitch Translate     |
|twitchTransFree_Win.exe |Binary for Windows for Twitch Translate   |

## First usage まず簡単に使いたい！
1:緑ボタン「clone or download」を押して，Download ZIPで全部ダウンロード  
2:解凍して，config.txtのTwitch_Channel を，翻訳したいチャンネルに書き換えて保存．  
3:twitchTransFree_(yourOS) をダブルクリック  
以上  

1:Press the green button "clone or download" and download it all with Download ZIP  
2: Extract and edit config.txt "Twitch_Channel" as a channel you want to translate.  
3: Double click on "twitchTransFree_(yourOS)"  

that's all  

## advertise 宣伝
This software is made for my wife!  
http://twitch.tv/saatan_pion/  
If you are satisfied by this software,
please watch my wife's stream! 
We are waiting for comming you! and 
subscribe! donation!

このソフトは，私の妻のために作りました．  
http://twitch.tv/saatan_pion/  
もしこのソフトが気に入ったら，私の妻の放送も見てください！
そして，サブスクライブやドネーションもお待ちしています．


## Introduction 説明
Twitchにて，チャットを自動で翻訳するPythonスクリプトです．

今は，設定ファイルにお試しで，翻訳ユーザ(saatan_trans）の設定を入れてあります．  
独自のアカウントを使いたいときには，AOUTHを取得して，config.txtを書き換えてください．  

This is a Python script to translate the chat text in Twitch automatically.

Currently, translation user (saatan_trans) is put in the setting file.  
To use your own account, please obtain AOUTH and rewrite config.txt.  



## ToDo 必要なもの

### Twitch OAUTH key
Go to following URL

https://twitchapps.com/tmi/

Generate OAUTH key!

Note: Please login to Twitch as a user who posts the translation result. In the case of my broadcast, I am making the user "translation chan: saatan_trans" for translating.

注意：翻訳結果を投稿するユーザでTwitchにログインしておいてください．私の放送の場合は「翻訳ちゃん：saatan_trans」というユーザにしています．


## config.txt 設定ファイル
```
Twitch_Channel          = #husband_sayonari_omega
Twitch_Username         = xxxxxxxxxx
Twitch_TextColor        = GoldenRod
Default_Language        = ja
Default_TransLanguage   = en

Twitch_OAUTH    = oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

`Twitch_Channel` : The target chat room for translation.  
`Twitch_Username` : User who posts translated text (It is better to create new user for translating).  
`Twitch_TextColor` : Text color of translate text.  
`Default_Language` : I recommend to set it to native language for streamer.  
`Default_TransLanguage` : I recommend to set it to the most used language in your chat room.  
`Twitch_OAUTH` : Twitch OAUTH key, you already get it at Section "Twitch OAUTH key".  

## USAGE 使い方
Write the necessary information in config.txt and execute twitchTrans.exe.

config.txtに必要な情報を書き込んで，twitchTransFree.exeを実行してください．

## secret 裏技
If you write `(language code):` at the beginning of the text of the chat, it will be translated into that language.

チャットのテキストの最初に `言語コード:` と記述すると，その言語に翻訳されます．
```
example 例

ko:I want to get money! ("ko" is language code of Korea.)
→　나는 돈을 갖고 싶다! 
```

support language サポート言語

https://cloud.google.com/translate/docs/languages

## Information of Developer 開発者情報

| | |
|:-|:-|
|Title       |Automatic Translator for Twitch Chat      |
|Developer   |husband_sayonari_omega                    |
|github      |https://github.com/sayonari/twitchTrans   |
|mail        |sayonari@gmail.com                        |

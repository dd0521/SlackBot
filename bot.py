import time
import re
from slackclient import SlackClient
 
# わたってきた単語によってそのアプリの最新バージョン返すとか
import versioncheck as verchk

class SlackBotMain:
 
    # Slackで取得したトークンを指定
    token = "xoxb-368257111252-367792160240-wiB21fFBErdcuhtuUe2bL052"#Workspace::yuichidev
    sc = SlackClient(token)
 
    def __init__(self):
        if SlackBotMain.sc.rtm_connect():
            while True:
                data = SlackBotMain.sc.rtm_read()
 
                if len(data) > 0:
                    for item in data:
                        SlackBotMain.sc.rtm_send_message("bottest", self.create_message(item))
 
                time.sleep(1)
        else:
            print ('Connection Failed, invalid token?') 
 
 
    def create_message(self, data):

        if "type" in data.keys():
            if data["type"] == "message":
                if data["text"].lower() == 'ver':
                    return 'yuichiBot Version1.0'
                elif data["text"].lower() == 'appver' or data["text"].lower() == 'app ver':
                    return "<@" + data["user"] + "> " + verchk.VersionCheckMain( 'FireFox' )
                elif re.search(u"(.*帰ります.*|.*帰宅.*)", data["text"]) is not None:
                    return "<@" + data["user"] + "> " + u"お疲れ様〜。気をつけて帰ってきてね！:wink:"
                elif re.search(u"(.*firefox.*|.*ふぁいあふぉっくす.*|.*ファイアフォックス.*)", data["text"].lower()) is not None:
                    return "<@" + data["user"] + "> " + verchk.VersionCheckMain( 'FireFox' )
                else:
                    return "<@" + data["user"] + "> " + u"\nAsk me\nfirefox"
 
 
sbm = SlackBotMain()
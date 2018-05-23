import re
import bs4
import urllib.request
from janome.tokenizer import Tokenizer
from selenium import webdriver

#########################################################################
# Utility functions 
def messageBox():
    from tkinter import Tk, messagebox

    root = Tk()
    root.withdraw()
    messagebox.showinfo('title', 'message')
    root.quit()

def split_sentence( sentence ):
    from janome.tokenizer import Tokenizer

    data = []

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize( sentence )

    for token in tokens:
        partOfSpeech = token.part_of_speech.split(',')[0]
        # 今回抽出するのは名詞だけとします。（もちろん他の品詞を追加、変更、除外可能です。）
        if partOfSpeech == u'名詞':
            data.append(token.surface )

    return data
"""
url='http://it-trend.jp/erp'
soup = bs4.BeautifulSoup( urllib.request.urlopen(url).read(),"html.parser")
title = soup.title.string
description = soup.find(attrs={"name":re.compile(r'Description',re.I)}).attrs['content']
h1=soup.h1.string
contents = title+description+h1
output_words=[]

print( split_sentence(contents) )
"""

#########################################################################
#   Version Ckeck functions
from distutils.version import StrictVersion

def getLatestVersionInfo_FireFox(url):
    soup = bs4.BeautifulSoup( urllib.request.urlopen(url).read(),"html.parser")
    # description = soup.find(attrs={"id":re.compile(r'main-content',re.I)})
    # 上みたいな書き方もできる
    # div<id="main-content">を探す
    description = soup.find("div", attrs={"id":"main-content"})
    # その中の<a>要素をすべて列挙
    versionList=description.find_all("a")

    verList = []
    for item in versionList:
        # from urllib.parse import urljoin

        # FireFoxのページから取得したバージョン一覧を吐き出し
        # slackbotに関してはいらん気もするからテスト終わったら消すかな～
        # urljoin → 第一引数(urlopenしたURL)と第二引数(取得した相対パス)をくっつけて絶対パスにする
        if( item.parent.name != 'strong' ):
            # print( item.string, urljoin(url,item.get("href")) )
            verList.append(item.string)
            # もともと配列に突っ込んでたけどFireFoxの場合は最初にとれるアイテムが最新ということでbreak
            break

    return 'FireFox: ' + verList[0]

def getLatestVersionInfo_Chrome(url):
    # http://phantomjs.org/download.html からそれぞれの環境に合わせたphantomJSのバイナリファイルを落としてくる。
    # 展開したフォルダの中のbinフォルダ内のphantomjs(windows版はphantomjs.exe)を下のスクリプトと同じ階層に入れる。
    # driver = webdriver.PhantomJS( executable_path='./bin/phantomjs' )みたいな感じでコピーしたバイナリの改装を合わせる
    driver = webdriver.PhantomJS( executable_path='./bin/phantomjs' )
    driver.get(url)
    # data = driver.page_source.encode('utf-8')
    # Chromeのバージョン情報がのるTableはJavascriptで動的生成されるので少し重いけどSeleniumで取得
    tags = driver.find_element_by_id('rows')
    rows = tags.find_elements_by_css_selector("tr")

    # rowはこんな順番なので条件判定して取りたいもの取得
    # os|channel|current_version|previous_version|current_reldate|previous_reldate|branch_base_commit|branch_base_position|branch_commit|true_branch|v8_version|changelog
    ret_x86_stable = None
    ret_x86_beta = None
    ret_x64_stable = None
    ret_x64_beta = None

    for row in rows:
        tdElements_row = row.find_elements_by_css_selector("td")
        # 最初に見つかったcurrent_versionを返す
        # for 32bit
        if( tdElements_row[0].text.lower() == 'win' ):
            if( tdElements_row[1].text.lower() == 'stable' and ret_x86_stable == None ):
                ret_x86_stable = tdElements_row[2].text
            elif( tdElements_row[1].text.lower() == 'beta' and ret_x86_beta == None ):
                ret_x86_beta = tdElements_row[2].text
        # for 64bit
        elif( tdElements_row[0].text.lower() == 'win' or tdElements_row[0].text.lower() == 'win64' ):
            if( tdElements_row[1].text.lower() == 'stable' and ret_x64_stable == None ):
                ret_x64_stable = tdElements_row[2].text
            elif( tdElements_row[1].text.lower() == 'beta' and ret_x64_beta == None ):
                ret_x64_beta = tdElements_row[2].text

        #ほしい情報全部取り終わった時点でbreak
        if( ret_x86_stable != None and ret_x86_beta != None and ret_x64_stable != None and ret_x64_beta != None ): 
            break
 
    return  'Chrome:\n'\
            'x86 Stable: ' + ret_x86_stable + '\n'\
            'x86 Beta: '+ ret_x86_beta + '\n'\
            'x64 Stable: ' + ret_x64_stable + '\n'\
            'x64 Beta: ' + ret_x64_beta

url_FireFox='https://www.mozilla.org/en-US/firefox/releases/'
# https://www.chromium.org/developers/calendarのiframeでここ参照してるけどとりまちょくせつ見にいく。
# 変わるようなら親(https://www.chromium.org/developers/calendar)から動的にとるかな
url_Chrome='https://omahaproxy.appspot.com/viewer'
def VersionCheckMain( _id ):
    if( _id == 'FireFox' ):        
        return getLatestVersionInfo_FireFox(url_FireFox)
    elif( _id == 'Chrome' ):
        return getLatestVersionInfo_Chrome(url_Chrome)
    else:
        return getLatestVersionInfo_Chrome(url_Chrome)
        


# test call
# VersionCheckMain('Chrome')



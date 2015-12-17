#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import gtk
import appindicator
import pynotify
import json
import os.path

class Person:
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

class CheckTime:
    def __init__(self):
        self.ind = appindicator.Indicator("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        self.python_script_path = os.path.abspath(os.path.dirname(__file__))
        self.ind.set_icon(self.python_script_path + "/icon/icon.svg")
        self.ind.set_label(" Github Account ")

        self.input_json()
        self.download_github_icon()

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def input_json(self):
        self.AccountList = []
        file_path = self.python_script_path + '/account/account.json'
        f = open(file_path, 'r')
        jsonData = json.load(f)

        #ここでキーをリスト化する。
        keyList = jsonData.keys()
        #キーでソートする
        keyList.sort()

        for k in keyList:
            # print k
            groupDict = jsonData[k]

            #ここでgroupListのキーを取得してnameListとする
            nameList = groupDict.keys()
            #これでキーである名前を並べ替え
            nameList.sort()

            for name in nameList:
                # print groupDict[name]
                one_acount = Person(k, groupDict[name])
                self.AccountList.append(one_acount)

        f.close()

    def download_github_icon(self):
        for i in range(0, len(self.AccountList)):
            file_name = self.AccountList[i].name + ".png"
            file_path = self.python_script_path + "/icon/" + file_name

            if os.path.exists(file_path) == False:
                print str(self.AccountList[i].name) + "のGithubアカウントのアイコンファイルが存在しません"
                print "ダウンロードします"
                github_img_url = "https://github.com/" + file_name
                cmd = "wget -O " + file_path + " " + github_img_url
                os.system(cmd)
                print str(self.AccountList[i].name) + "のアイコンダウンロード完了"

    def menu_setup(self):
        self.menu = gtk.Menu()
        for i in range(0, len(self.AccountList)):
            self.account_item = gtk.MenuItem(self.AccountList[i].name)
            self.account_item.connect("activate", self.change_action, self.AccountList[i])
            self.account_item.show()
            self.menu.append(self.account_item)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def change_action(self, widget, p):
        pynotify.init(p.name)
        msg = "Githubアカウントを" + p.name + "に切り替えました"
        img_name = self.python_script_path + "/icon/" + p.name + ".png"
        self.nty = pynotify.Notification(msg, "", os.path.abspath(img_name))

        name_and_space = " " + p.name + " "
        self.ind.set_label(name_and_space)

        config_name = "git config --global user.name \"" + p.name + "\""
        config_email = "git config --global user.email \"" + p.mail + "\""
        os.system(config_name)
        os.system(config_email)

        self.nty.show()

if __name__ == "__main__":
    indicator = CheckTime()
    indicator.main()
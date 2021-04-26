import os
import re
import threading
import win32api
from PyQt5 import QtWidgets, QtGui, QtCore
from asrInterface import Ui_MainWindow
import sys
import speech_recognition as sr


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.now_choose = "sphinx"
        self.now_choose_lan = "en"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.recognize_btn.clicked.connect(self.listen_thread)
        self.ui.sphinx_bar.triggered.connect(self.choose_sphinx)
        self.ui.google_bar.triggered.connect(self.choose_google)
        # self.ui.bing_bar.triggered.connect(self.choose_bing)
        self.ui.cn_bar.triggered.connect(self.choose_cn)
        self.ui.en_bar.triggered.connect(self.choose_en)

    def listen_thread(self):
        if self.now_choose_lan == "en":
            self.ui.label.setText("I'm listening...")
        elif self.now_choose_lan == "cn":
            self.ui.label.setText("请说，我在听...")
        t = threading.Thread(target=self.listen)
        t.setDaemon(True)
        t.start()
        self.ui.recognize_btn.setStyleSheet(
            "QPushButton{border-image: url(icon/play.gif);}"
        )
        self.ui.recognize_btn.setEnabled(False)

    def listen(self):
        r = sr.Recognizer()
        text = ""
        mic = sr.Microphone(device_index=1)
        with mic as source:
            # 降噪
            r.adjust_for_ambient_noise(source)
            audio = r.record(mic, duration=5)
        try:

            if self.now_choose_lan == "en":
                self.ui.label.setText("Identifying...")
            elif self.now_choose_lan == "cn":
                self.ui.label.setText("识别中...")

            # 可选sphinx\google\模式
            # 其中google需要科学上网
            # 废弃bing，因为需要api密钥
            if self.now_choose_lan == "en":
                if self.now_choose == "google":
                    text = r.recognize_google(audio)
                elif self.now_choose == "sphinx":
                    text = r.recognize_sphinx(audio)
            elif self.now_choose_lan == "cn":
                if self.now_choose == "google":
                    text = r.recognize_google(audio, language="zh-cn")
                elif self.now_choose == "sphinx":
                    text = r.recognize_sphinx(audio, language="zh-cn")

            self.cmd(text)
            self.ui.set_recognize_btn_style()
            self.ui.recognize_btn.setEnabled(True)

        except BaseException as e:
            print(e)
            if self.now_choose_lan == "en":
                self.ui.label.setText("Please speak again~")
            elif self.now_choose_lan == "cn":
                self.ui.label.setText("我没有听清楚，请再说一遍呢~")
            self.ui.set_recognize_btn_style()
            self.ui.recognize_btn.setEnabled(True)

    def cmd(self, text):
        text=text.lower()
        CMD1 = ["music", "listen", "play", "播放", "听", "音乐"]
        CMD2 = ["text", "edit", "notepad", "note", "编辑", "记事本"]

        is_cmd_music = False
        is_cmd_text = False
        for cmd1 in CMD1:
            if re.search(cmd1, text):
                is_cmd_music = True
                break
        for cmd2 in CMD2:
            if re.search(cmd2, text):
                is_cmd_text = True
                break
        if is_cmd_music:
            if self.now_choose_lan == "en":
                self.ui.label.setText("You said \""+text+"\" \n I'll play music for you~")
            elif self.now_choose_lan == "cn":
                self.ui.label.setText("您说了\""+text+"\"\n马上为您播放音乐~")
            win32api.ShellExecute(0, "open", os.getcwd() + "\\music\\1.mp3", "", "", 1)

        elif is_cmd_text:
            if self.now_choose_lan == "en":
                self.ui.label.setText("You said \""+text+"\" \n I'll open notepad for you~")
            elif self.now_choose_lan == "cn":
                self.ui.label.setText("您说了\""+text+"\"\n马上为您打开记事本~")
            win32api.ShellExecute(0, "open", "notepad.exe", "", "", 1)
        else:
            if self.now_choose_lan == "en":
                self.ui.label.setText("You said \"" + text + "\" \nbut I can't understand")
            elif self.now_choose_lan == "cn":
                self.ui.label.setText("您说了\"" + text + "\" \n但是我不明白您的意思呢~")

    def choose_sphinx(self):
        self.ui.sphinx_bar.setChecked(True)
        self.ui.google_bar.setChecked(False)
        # self.ui.bing_bar.setChecked(False)

        if self.now_choose_lan == "en":
            self.ui.label.setText("You change the Trans-API to Sphinx.")
        elif self.now_choose_lan == "cn":
            self.ui.label.setText("您已将语言识别API切换为Sphinx")

        self.ui.set_recognize_btn_style()
        self.ui.recognize_btn.setEnabled(True)

        self.ui.sphinx_action.setText(" √  Sphinx  ")
        self.ui.set_style(self.ui.sphinx_action)

        self.ui.google_action.setText("     Google  ")
        self.ui.set_style(self.ui.google_action)

        '''
        self.ui.google_action.setText("     Bing  ")
        self.ui.set_style(self.ui.bing_action)
        '''

        self.now_choose = "sphinx"

    def choose_google(self):
        self.ui.sphinx_bar.setChecked(False)
        self.ui.google_bar.setChecked(True)
        # self.ui.bing_bar.setChecked(False)

        if self.now_choose_lan == "en":
            self.ui.label.setText("You change the Trans-API to Google.")
        elif self.now_choose_lan == "cn":
            self.ui.label.setText("您已将语言识别API切换为Google")

        self.ui.set_recognize_btn_style()
        self.ui.recognize_btn.setEnabled(True)

        self.ui.sphinx_action.setText("     Sphinx  ")
        self.ui.set_style(self.ui.sphinx_action)

        self.ui.google_action.setText(" √  Google  ")
        self.ui.set_style(self.ui.google_action)

        '''
        self.ui.bing_action.setText("     Bing  ")
        self.ui.set_style(self.ui.bing_action)
        '''

        self.now_choose = "google"

    '''
    def choose_bing(self):
        self.ui.sphinx_bar.setChecked(False)
        self.ui.google_bar.setChecked(False)
        self.ui.bing_bar.setChecked(True)

        self.ui.label.setText("You change the Trans-API to Bing.")

        self.ui.set_recognize_btn_style()

        self.ui.sphinx_action.setText("   Sphinx  ")
        self.ui.set_style(self.ui.sphinx_action)

        self.ui.google_action.setText("    Google  ")
        self.ui.set_style(self.ui.google_action)

        self.ui.bing_action.setText(" √   Bing  ")
        self.ui.set_style(self.ui.bing_action)

        self.now_choose = "bing"
    '''

    def choose_cn(self):
        self.ui.cn_bar.setChecked(True)
        self.ui.en_bar.setChecked(False)

        self.ui.label.setText("您已经将识别语言切换为中文~")

        self.ui.set_recognize_btn_style()
        self.ui.recognize_btn.setEnabled(True)

        self.ui.en_action.setText("        English  ")
        self.ui.set_style(self.ui.en_action)

        self.ui.cn_action.setText("  √    中文  ")
        self.ui.set_style(self.ui.cn_action)

        self.ui.cn_ui_text()

        self.now_choose_lan = "cn"

    def choose_en(self):
        self.ui.cn_bar.setChecked(False)
        self.ui.en_bar.setChecked(True)

        self.ui.label.setText("You change the language to English~")

        self.ui.set_recognize_btn_style()
        self.ui.recognize_btn.setEnabled(True)

        self.ui.en_action.setText("  √    English  ")
        self.ui.set_style(self.ui.en_action)

        self.ui.cn_action.setText("       中文  ")
        self.ui.set_style(self.ui.cn_action)

        self.ui.en_ui_text()

        self.now_choose_lan = "en"


app = QtWidgets.QApplication([])
application = myWindow()
application.show()
sys.exit(app.exec())

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 900)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 设置菜单栏
        self.menu_bar = QMainWindow.menuBar(MainWindow)
        # 添加菜单——模式按钮：可选sphinx\google模式
        # 其中google需要科学上网
        self.model_bar = self.menu_bar.addMenu("Model")
        # 添加菜单——语言按钮：可选中文\English模式
        self.language_bar = self.menu_bar.addMenu("Language")

        self.menu_bar.setFont(QtGui.QFont('Microsoft YaHei', 9))
        self.menu_bar.setStyleSheet(
            "QMenuBar::item {font-size: 10pt;color: rgb(225,225,225);background-color:rgb(50,50,50)}"
            "QMenuBar::item:selected {background-color:rgb(0,117,210);}"
            "QMenuBar::item:pressed {border: 1px solid rgb(60,60,61); background-color: rgb(0,117,210); } "
        )

        # 设置Model的两个子菜单
        # sphinx Trans-API
        self.sphinx_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.sphinx_bar.setChecked(True)
        self.sphinx_action = QtWidgets.QLabel(" √  Sphinx  ")
        self.set_style(self.sphinx_action)
        self.sphinx_bar.setDefaultWidget(self.sphinx_action)

        # google Trans-API
        self.google_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.google_bar.setChecked(False)
        self.google_action = QtWidgets.QLabel("     Google  ")
        self.set_style(self.google_action)
        self.google_bar.setDefaultWidget(self.google_action)

        '''
        # bing Trans-API
        self.bing_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.bing_bar.setChecked(False)
        self.bing_action = QtWidgets.QLabel("     Bing  ")
        self.set_style(self.bing_action)
        self.bing_bar.setDefaultWidget(self.bing_action)
        '''

        # 向LanguageBar小控件中添加按钮，子菜单
        # EN -API
        self.en_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.en_bar.setChecked(True)
        self.en_action = QtWidgets.QLabel("  √   English  ")
        self.set_style(self.en_action)
        self.en_bar.setDefaultWidget(self.en_action)

        # CN -API
        self.cn_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.cn_bar.setChecked(False)
        self.cn_action = QtWidgets.QLabel("       中文  ")
        self.set_style(self.cn_action)
        self.cn_bar.setDefaultWidget(self.cn_action)

        # 将按钮添加到model_bar中去
        self.model_bar.addAction(self.sphinx_bar)
        self.model_bar.addAction(self.google_bar)
        # self.model_bar.addAction(self.bing_bar)

        # 将按钮加到language_bar中去
        self.language_bar.addAction(self.en_bar)
        self.language_bar.addAction(self.cn_bar)

        # 创建语音识别开始按钮，并将按钮加入到窗口MainWindow中
        self.recognize_btn = QtWidgets.QPushButton(MainWindow)  # 创建一个按钮，并将按钮加入到窗口MainWindow中
        self.recognize_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.recognize_btn.setGeometry(210, 780, 80, 80)
        self.set_recognize_btn_style()

        # 加载动态图片
        self.voiceFig = QtWidgets.QLabel(self.centralwidget)
        self.voiceFig.setGeometry(QtCore.QRect(50, 50, 400, 300))
        self.voiceFig.setText("")
        self.gif = QMovie("icon/voice.gif")
        self.voiceFig.setMovie(self.gif)
        self.gif.start()
        self.voiceFig.setScaledContents(True)
        self.voiceFig.setObjectName("voiceFig")

        # Hi! How can I help?
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 350, 400, 230))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 117, 210);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        # You can:
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(25, 580, 450, 50))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        # 1. Enjoy music by saying \"Play music\"
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 630, 400, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        # 2. Take some notes by saying \"Open Notepad\"
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 670, 400, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_recognize_btn_style(self):
        self.recognize_btn.setStyleSheet("QPushButton{border-image: url(icon/phone.png);}"
                                         "QPushButton:hover{border-image: url(icon/phone-hover.png);}"
                                         "QPushButton:pressed{border-image: url(icon/play.gif)}")

    def set_style(self, ui):
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        ui.setFont(font)
        ui.setStyleSheet(
            "QLabel { color: rgb(225,225,225);background-color:rgb(50,50,50);}"
            "QLabel:hover{ color: rgb(225,225,225);background-color:rgb(0,117,210);}"
        )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "语音助手"))
        self.label.setText(_translate("MainWindow", "Hi! How can I help?"))
        self.label_2.setText(_translate("MainWindow", "You can say:"))
        self.label_3.setText(_translate("MainWindow", "1. \"Play music\" or \"Listen Music\""))
        self.label_4.setText(_translate("MainWindow", "2. \"Open Notepad\" or \"Edit Text\""))

    def cn_ui_text(self):
        self.label.setText("嗨! 我能帮您什么?")
        self.label_2.setText("您可以说:")
        self.label_3.setText("1. \"我要听音乐\"或\"播放音乐\" ")
        self.label_4.setText("2. \"打开记事本\"或\"我要编辑\" ")
        self.model_bar.setTitle("模式")
        self.language_bar.setTitle("语言")

    def en_ui_text(self):
        self.label.setText("Hi! How can I help?")
        self.label_2.setText("You can say:")
        self.label_3.setText("1. \"Play music\" or \"Listen Music\"")
        self.label_4.setText("2. \"Open Notepad\" or \"Edit Text\"")
        self.model_bar.setTitle("Model")
        self.language_bar.setTitle("Language")

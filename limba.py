# from github import Github
import threading
import json
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon, QPalette, QColor, QMovie, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, \
    QFrame, QLabel, QPlainTextEdit, QTextEdit, QScrollArea, QGraphicsView, QDockWidget, QListWidgetItem, QListWidget
from PyQt5.uic.properties import QtGui
from PyQt5.uic.properties import QtGui
from PySide2.QtCore import SIGNAL

from Limbo.style import *
from Limbo.tools import *

class guii(QMainWindow):
    def __init__(gui):
        super().__init__()
        gui.addInf = "0"
        gui.setMinimumSize(500, 650)
        gui.setBaseSize(500, 200)
        gui.setWindowFlag(Qt.FramelessWindowHint)
        gui.setWindowTitle("Limbo")
        gui.setWindowIcon(QIcon(getPath("data/media/logo.ico")))

        # strs
        gui.isFull = 0
        gui.typeList = "note"

        # prestatusbar
        gui.statusBarCl = QPushButton(QIcon(getPath("data/media/cansel.ico")), "")
        gui.statusBarCl.setStyleSheet(
            "QPushButton{background-color: '#80FFFFFF';  border: 0px #80FFFFFF;" "border-radius: 10px;}")

        # statusbar
        gui.statusBar().showMessage("Загрузка. Ждите")
        gui.statusBar().setStyleSheet("background-image: url(" + getPath("data/media/horse.ico") +");")
        gui.statusBar().addPermanentWidget(gui.statusBarCl)
        gui.statusBarCl.clicked.connect(lambda: gui.statusBar().hide())

        # menuBar(topBar)
        gui.topbar = gui.menuBar()
        gui.topbar.setStyleSheet("background-color: '#DEDEDE';")
        gui.fileMenu = gui.topbar.addMenu("&File")
        gui.gitMenu = gui.topbar.addMenu("&Git")
        gui.fireMenu = gui.topbar.addMenu("&Firebase")
        gui.jsonMenu = gui.topbar.addMenu("&JSON")
        gui.socketMenu = gui.topbar.addMenu("&Sockets")
        gui.exitA = QAction(QIcon(getPath("data/media/exit.ico")), "&Exit", gui)
        gui.fullscreen = QAction(QIcon(getPath("data/media/gull.png")), "&FullScreen", gui)
        gui.terminal = QAction(QIcon(getPath("data/media/terminal.png")), "&Terminal", gui)
        gui.gitLogin = QAction(QIcon(getPath('data/media/git.ico')), "&Sign In", gui)
        gui.gitInstall = QAction(QIcon(getPath("data/media/git.ico")), "&Install", gui)
        gui.fireLogin = QAction(QIcon(getPath("data/media/fire.ico")), "&Sing In", gui)
        gui.fireUpdate = QAction(QIcon(getPath("data/media/fire.ico")), "&Update", gui)
        gui.jsonUpdate = QAction(QIcon(getPath("data/media/json.png")), "&Load", gui)
        gui.jsonEdit = QAction(QIcon(getPath("data/media/json.png")), "&Upload", gui)
        gui.socketOn = QAction(QIcon(getPath("data/media/send.ico")), "&Off Socket")
        gui.exitA.setShortcut("Ctrl+Q")
        gui.fullscreen.setShortcut("F11")
        gui.exitA.triggered.connect(QCoreApplication.instance().quit)
        gui.gitLogin.triggered.connect(gui.gitVisLog)
        gui.jsonUpdate.triggered.connect(gui.jsonLoad)
        gui.jsonEdit.triggered.connect(gui.jsonUpload)
        gui.fireLogin.triggered.connect(gui.firebaseAuth)
        gui.fullscreen.triggered.connect(gui.fulldisplay)

        gui.fileMenu.addAction(gui.fullscreen)
        gui.fileMenu.addAction(gui.terminal)
        gui.fileMenu.addAction(gui.exitA)
        gui.gitMenu.addAction(gui.gitLogin)
        gui.gitMenu.addAction(gui.gitInstall)
        gui.fireMenu.addAction(gui.fireLogin)
        gui.fireMenu.addAction(gui.fireUpdate)
        gui.jsonMenu.addAction(gui.jsonUpdate)
        gui.jsonMenu.addAction(gui.jsonEdit)
        gui.socketMenu.addAction(gui.socketOn)
        gui.gitInstall.setEnabled(False)
        gui.fireUpdate.setEnabled(False)

        # toolbar
        gui.log = QLineEdit()
        gui.pas = QLineEdit()
        gui.go = QAction(QIcon(getPath("data/media/gitLog.ico")), "&Sign in", gui)
        gui.toolbar = gui.addToolBar("")
        gui.toolbar.setVisible(False)
        gui.start()
        gui.show()

    def start(gui):
        def updateList():
            if os.path.exists("../data.limbo"):
                with open("../data.limbo", "r") as read_file:
                    gui.data = json.loads(read_file.read())
                    read_file.close()
                    for neme, des, type in gui.data:
                        gui.myQListWidgetItem = QListWidgetItem(gui.noteListItems)
                        gui.myQListWidgetItem.setHidden(True)
                        if type == 'note':
                            gui.myQCustomQWidget.setTextUp(neme)
                            gui.myQCustomQWidget.setTextDown(des)
                            gui.myQCustomQWidget.setIcon(getPath("data/media/edit.ico"))
                            if gui.typeList == 'note':
                                gui.myQListWidgetItem.setHidden(False)
                        elif type == "code":
                            gui.myQCustomQWidget.setTextUp(neme)
                            gui.myQCustomQWidget.setTextDown(des)
                            gui.myQCustomQWidget.setIcon(getPath("data/media/code.icon.webp"))
                            if gui.typeList == 'code':
                                gui.myQListWidgetItem.setHidden(False)

                        gui.myQListWidgetItem.setSizeHint(gui.myQCustomQWidget.sizeHint())
                        gui.noteListItems.setItemWidget(gui.myQListWidgetItem, gui.myQCustomQWidget)
                        gui.noteListItems.addItem(gui.myQListWidgetItem)
                    gui.noteListItems.itemClicked.connect(gui.infoPost)
                    gui.list_block.addLayout(gui.tab_but)
                    gui.list_block.addWidget(gui.noteListItems)
                    gui.frame_List.setLayout(gui.list_block)

        def noteClck():
            gui.codeTab.setStyleSheet(styleStartTabs)
            gui.typeList = "note"
            gui.noteTab.setStyleSheet(styleStartTabs_selected)
            gui.noteListItems.clear()

            gui.myQCustomQWidget = QCustomQWidget(gui)
            gui.myQCustomQWidget.setStyleSheet(styleMyQCustomQWidget)
            threading.Thread(target=updateList).start()

        def codeClck():
            gui.noteTab.setStyleSheet(styleStartTabs)
            gui.typeList = "code"
            gui.codeTab.setStyleSheet(styleStartTabs_selected)
            gui.noteListItems.clear()

            gui.myQCustomQWidget = QCustomQWidget(gui)
            gui.myQCustomQWidget.setStyleSheet(styleMyQCustomQWidget)
            threading.Thread(target=updateList).start()

        gui.tab_but = QHBoxLayout()
        gui.fab = QPushButton(QIcon(getPath("data/media/add.png")), "")
        gui.fab.setStyleSheet("background-color: white; border: 1px white;")
        gui.list_block = QVBoxLayout()
        gui.fab_block = QHBoxLayout()
        gui.fab_block.addStretch(1)
        gui.fab_block.addWidget(gui.fab)
        gui.vbox = QVBoxLayout(gui)
        gui.frame_List = QScrollArea()
        gui.frame_List.setStyleSheet("QScrollArea {background-color: white;  border: 2px white;" "border-radius: 7px;}")
        gui.frame_Fab = QFrame()
        gui.frame_Fab.setLayout(gui.fab_block)
        gui.vbox.addWidget(gui.frame_List)
        gui.vbox.addWidget(gui.frame_Fab)
        gui.fab.clicked.connect(gui.addInfo)
        gui.frame_vbox = QFrame()
        gui.frame_vbox.setLayout(gui.vbox)
        gui.setCentralWidget(gui.frame_vbox)
        gui.setStyleSheet("background-color: white;")
        gui.noteTab = QPushButton("Note")
        gui.codeTab = QPushButton("Code")
        gui.codeTab.setStyleSheet(styleStartTabs)
        gui.noteTab.setStyleSheet(styleStartTabs)
        gui.noteTab.clicked.connect(noteClck)
        gui.codeTab.clicked.connect(codeClck)
        gui.tab_but.addWidget(gui.noteTab)
        gui.tab_but.addWidget(gui.codeTab)
        gui.tab_but.addStretch(1)
        gui.noteListItems = QListWidget()
        if gui.typeList == "code":
            gui.codeTab.setStyleSheet(styleStartTabs_selected)
        if gui.typeList == "note":
            gui.noteTab.setStyleSheet(styleStartTabs_selected)
        gui.myQCustomQWidget = QCustomQWidget(gui)
        gui.myQCustomQWidget.setStyleSheet(styleMyQCustomQWidget)
        threading.Thread(target=updateList).start()

    def gitVisLog(gui):
        layBody = QHBoxLayout()
        preSkelet = QFrame()
        skelet = QVBoxLayout()
        preBody = QFrame()
        preBody.setMaximumWidth(700)
        preBody.setMinimumWidth(450)
        body = QVBoxLayout()
        login = QLineEdit()
        password = QLineEdit()
        buttons = QHBoxLayout()
        login.setPlaceholderText(u'Login/Email')
        password.setPlaceholderText(u'password')
        ok = QPushButton(QIcon(getPath("data/media/ok.ico")), "Login")
        cansel = QPushButton(QIcon(getPath("data/media/cansel.ico")), "")
        logo = QPushButton(QIcon(getPath("data/media/git.ico")), "")
        ok.setFixedWidth(100)
        password.setEchoMode(QLineEdit.Password)
        logo.setStyleSheet("QPushButton{background-color: '#C0C8DB';  border: 2px #C0C8DB;" "border-radius: 10px;}")
        login.setStyleSheet("QLineEdit {background-color: '#EDEDED';  border: 0px #EDEDED;" "border-radius: 10px;}")
        password.setStyleSheet("QLineEdit {background-color: '#EDEDED';  border: 0px #EDEDED;" "border-radius: 10px;}")
        ok.setStyleSheet("QPushButton{background-color: '#EDEDED';  border: 0px #EDEDED;" "border-radius: 10px;}")
        cansel.setStyleSheet("QPushButton{background-color: '#EDEDED';  border: 0px #EDEDED;" "border-radius: 10px;}")
        cansel.clicked.connect(gui.start)
        body.addWidget(logo)
        body.addWidget(login)
        body.addWidget(password)
        buttons.addStretch(1)
        buttons.addWidget(cansel)
        buttons.addWidget(ok)
        body.addLayout(buttons)
        preBody.setStyleSheet("QFrame{background-color: '#C0C8DB';  border: 2px #C0C8DB;" "border-radius: 10px;}")
        preBody.setLayout(body)
        layBody.addStretch(1)
        layBody.addWidget(preBody)
        layBody.addStretch(1)
        skelet.addLayout(layBody)
        skelet.addStretch(1)
        preSkelet.setLayout(skelet)
        gui.setCentralWidget(preSkelet)

    def jsonLoad(gui):
        print('яддяфыц')

    def jsonUpload(gui):
        print('Не нужно')

    def addInfo(gui):
        def translate(text):
            gui.translate.setIcon(QIcon(getPath("data/media/loading.ico")))
            from googletrans import Translator
            from textblob import TextBlob
            import threading
            trans = Translator()

            def potok():
                try:
                    if TextBlob(text).detect_language() == 'en':
                        pr = trans.translate(text=text, scr='en', dest='ru')
                        gui.desEdit.setText(pr.text)
                    elif TextBlob(text).detect_language() == 'ru':
                        pr = trans.translate(text=text, scr='ru', dest='en')
                        gui.desEdit.setText(pr.text)
                    else:
                        gui.desEdit.setText("Error")
                    gui.translate.setIcon(QIcon(getPath("data/media/translate.ico")))
                except:
                    potok()

            threading.Thread(target=potok).start()

        if gui.addInf == "0":
            gui.fab.hide()
            gui.nameEdit = QLineEdit()
            gui.nameEdit.setPlaceholderText(u'Название')
            gui.nameEdit.setStyleSheet(
                "QLineEdit {background-color: '#DEDEDE';  border: 2px solid grey;" "border-radius: 7px;}")
            gui.desEdit = QLineEdit()
            gui.desEdit.setPlaceholderText(u'Описание')
            gui.desEdit.setStyleSheet(
                "QLineEdit {background-color: '#DEDEDE';  border: 2px solid grey;" "border-radius: 7px;}")
            gui.addBlock = QVBoxLayout()
            gui.frame_Add = QFrame()
            gui.frame_Add.setLayout(gui.addBlock)
            gui.widget = QWidget()
            gui.frame_Add.setStyleSheet("QWidget {background-color: grey;  border: 0px grey;" "border-radius: 10px;}")
            gui.addBlock.addWidget(gui.nameEdit)
            gui.addBlock.addWidget(gui.desEdit)
            gui.more = QPushButton(QIcon(getPath("data/media/edit.ico")), "")
            gui.send = QPushButton(QIcon(getPath("data/media/send.ico")), "")
            gui.translate = QPushButton(QIcon(getPath("data/media/translate.ico")), "")
            gui.more.setStyleSheet("background-color: white; border: 1px white;")
            gui.send.setStyleSheet("background-color: white; border: 1px white;")
            gui.translate.setStyleSheet("background-color: white; border: 1px white;")
            gui.send.clicked.connect(gui.sendMsg)
            gui.translate.clicked.connect(lambda: translate(gui.nameEdit.text()))
            fabL = QVBoxLayout()
            fabL.addWidget(gui.more)
            fabL.addWidget(gui.send)
            fabL.addWidget(gui.translate)
            gui.frame_fabL = QFrame()
            gui.frame_fabL.setLayout(fabL)
            gui.more.clicked.connect(gui.moreInfo)
            gui.fab_block.addWidget(gui.frame_Add)
            gui.fab_block.addWidget(gui.frame_fabL)
            gui.addInf = 'ok'

    def moreInfo(gui):
        gui.type = 'note'

        def noteClk():
            gui.type = "note"
            gui.noteBut.setText("V")
            gui.codeBut.setText("")
            gui.desMore.setPlaceholderText(u"Описание")

        def codeClk():
            gui.type = "code"
            gui.noteBut.setText("")
            gui.codeBut.setText("V")
            gui.desMore.setPlaceholderText(u"Код")

        def pasteBuf():
            import pyperclip
            gui.desMore.setText(pyperclip.paste())

        gui.frame_vbox.hide()
        gui.nameMore = QLineEdit()
        gui.desMore = QTextEdit()
        gui.nameMore.setPlaceholderText(u'Название')
        gui.desMore.setPlaceholderText(u'Описание')
        gui.nameMore.setStyleSheet(
            "QLineEdit {background-color: '#DEDEDE';  border: 2px solid grey;" "border-radius: 7px;}")
        gui.desMore.setStyleSheet(
            "QTextEdit {background-color: '#DEDEDE';  border: 2px solid grey;" "border-radius: 7px;}")
        gui.nameMore.setText(gui.nameEdit.text())
        gui.desMore.setText(gui.desEdit.text())
        gui.okey = QPushButton(QIcon(getPath("data/media/ok.ico")), "")
        gui.cansel = QPushButton(QIcon(getPath("data/media/cansel.ico")), "")
        gui.noteBut = QPushButton(QIcon(getPath("data/media/note.png")), "V")
        gui.codeBut = QPushButton(QIcon(getPath("data/media/code.png")), "")
        gui.pasteBut = QPushButton(QIcon(getPath("data/media/pastee.ico")), "")
        gui.okey.setStyleSheet(styleButs_MoreInfo)
        gui.cansel.setStyleSheet(styleButs_MoreInfo)
        gui.noteBut.setStyleSheet(styleButs_MoreInfo)
        gui.codeBut.setStyleSheet(styleButs_MoreInfo)
        gui.pasteBut.setStyleSheet(styleButs_MoreInfo)
        gui.okey.clicked.connect(gui.addPost)
        gui.cansel.clicked.connect(gui.start)
        gui.noteBut.clicked.connect(noteClk)
        gui.codeBut.clicked.connect(codeClk)
        gui.pasteBut.clicked.connect(pasteBuf)
        vbox2 = QVBoxLayout()
        name_block = QHBoxLayout()
        name_block.addWidget(gui.nameMore)
        name_block.addWidget(gui.pasteBut)
        vbox2.addLayout(name_block)
        vbox2.addWidget(gui.desMore)
        vbox1 = QHBoxLayout()
        vbox1.addWidget(gui.noteBut)
        vbox1.addWidget(gui.codeBut)
        vbox1.addStretch(1)
        vbox1.addWidget(gui.cansel)
        vbox1.addWidget(gui.okey)
        vbox2.addLayout(vbox1)
        gui.vbox2 = QFrame()
        gui.vbox2.setStyleSheet("QWidget {background-color: grey;  border: 0px grey;" "border-radius: 10px;}")
        gui.vbox2.setLayout(vbox2)
        gui.setCentralWidget(gui.vbox2)

    def sendMsg(gui):
        import socket
        import threading
        sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_glav = socket.gethostbyname(socket.gethostname())
        ip = ip_glav[0:11]
        name = os.getlogin
        sok.bind(("", 0))
        n = "None"
        for i in range(256):
            if n == "None":
                def potok():
                    ser = ip + str(i), 9090
                    try:
                        print(ser)
                        sok.connect(ser)
                        sok.send((name + "Connected").encode("utf-8"))
                        sok.send((name + gui.nameEdit.text() + ",&," + gui.desEdit.text()).encode("utf-8"))
                        n == "Ok"
                        gui.statusBar().showMessage("Connect: " + str(ser))
                    except:
                        print("Ошибка с: ", ser)
                        if i == 255:
                            gui.statusBar().show()
                            gui.statusBar().showMessage("Не найдены хосты")
                        pass

                pot = threading.Thread(target=potok)
                pot.start()
            if n == "Ok":
                i = 255

    def addPost(gui):
        import threading
        def potok():
            if os.path.exists("../data.limbo"):
                with open("../data.limbo", "r") as read_file:
                    data = json.loads(read_file.read())
                print(data)
                gui.vbox2.hide()
                c = ()
                name = gui.nameMore.text()
                des = gui.desMore.toPlainText()
                c = (name, des, gui.type)
                data.append(c)
                print(data)
                read_file.close()
                with open("../data.limbo", "w") as write_file:
                    json.dump(data, write_file)
                write_file.close()
                gui.start()
            else:
                data = []
                c = ()
                name = gui.nameMore.text()
                des = gui.desMore.toPlainText()
                c = (name, des)
                data.append(c)
                with open("../data.limbo", "w") as write_file:
                    json.dump(data, write_file)
                write_file.close()
                gui.start()

        pot = threading.Thread(target=potok)
        pot.start()

    def infoPost(gui, int):
        def playCode(text):
            import subprocess, os, platform
            filepath = "data/output/start.py"
            handle = open(filepath, "w")
            handle.write(text)
            handle.close()
            filepath = os.path.abspath(filepath)
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', filepath))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(filepath)
            else:  # linux variants
                subprocess.call(('xdg-open', filepath))

        def deliteList(data, int):
            def ok():
                data.pop(int)
                with open("../data.limbo", "w") as write_file:
                    json.dump(data, write_file)
                write_file.close()
                gui.start()

            gui.delite.setText("Удалить?")
            gui.delite.setStyleSheet(styleDelite)
            gui.delite.clicked.connect(ok)

        def copyBuf(text):
            import pyperclip
            import time
            import threading

            pyperclip.copy(text)
            gui.copy.setText("Скопито")

            def hide():
                time.sleep(1)
                gui.copy.setText("")

            threading.Thread(target=hide).start()

        int = gui.noteListItems.currentRow()
        cansel = QPushButton(QIcon(getPath("data/media/cansel.ico")), "")
        cansel.setStyleSheet(styleButs_InfoPost)
        cansel.clicked.connect(gui.start)
        gui.delite = QPushButton(QIcon(getPath("data/media/delite.svg")), "")
        gui.delite.setStyleSheet(styleButs_InfoPost)
        gui.delite.clicked.connect(lambda: deliteList(gui.data, int))
        gui.copy = QPushButton(QIcon(getPath("data/media/pastee.ico")), "")
        gui.copy.setStyleSheet(styleButs_InfoPost)
        gui.copy.clicked.connect(lambda: copyBuf(info[1]))
        gui.play = QPushButton(QIcon(getPath("data/media/play.png")), "")
        gui.play.setStyleSheet(styleButs_InfoPost)
        gui.play.clicked.connect(lambda: playCode(info[1]))
        preBody = QFrame()
        body = QVBoxLayout()
        nameBlock = QHBoxLayout()
        preSkelet = QFrame()
        skelet = QVBoxLayout()
        info = gui.data[int]
        name = QLabel(info[0])
        des = QLabelScroll(gui)
        des.setText(info[1])
        fontName = QFont()
        fontName.setBold(True)
        name.setFont(fontName)
        nameBlock.addWidget(name)
        nameBlock.addStretch(1)
        if info[2] == 'code':
            nameBlock.addWidget(gui.play)
        nameBlock.addWidget(gui.copy)
        nameBlock.addWidget(gui.delite)
        nameBlock.addWidget(cansel)
        body.addLayout(nameBlock)
        body.addWidget(des)
        preBody.setLayout(body)
        preBody.setStyleSheet(stylePreBody)
        skelet.addStretch(1)
        skelet.addWidget(preBody)
        preSkelet.setLayout(skelet)
        gui.setCentralWidget(preSkelet)

    def fulldisplay(gui):
        if gui.isFull == 1:
            gui.showNormal()
            gui.isFull = 0
        else:
            gui.showFullScreen()
            gui.isFull = 1

    def firebaseAuth(gui):

        def login():
            from Limbo.more.Firebase.Firebase import FirebaseInit

            def potok():
                LOGIN = gui.login.text()
                PASSWORD = gui.password.text()
                Firebasee = FirebaseInit(LOGIN, PASSWORD)
                print(Firebasee)

            threading.Thread(target=potok).start()


        preSkelet = QFrame()
        layBody = QHBoxLayout()
        skelet = QVBoxLayout()
        preBody = QFrame()
        preBody.setMaximumWidth(700)
        preBody.setMinimumWidth(450)
        body = QVBoxLayout()
        gui.login = QLineEdit()
        gui.password = QLineEdit()
        buttons = QHBoxLayout()
        gui.login.setPlaceholderText(u'Login/Email')
        gui.password.setPlaceholderText(u'password')
        ok = QPushButton(QIcon(getPath("data/media/ok.ico")), "Login")
        cansel = QPushButton(QIcon(getPath("data/media/cansel.ico")), "")
        logo = QPushButton(QIcon(getPath("data/media/fire.ico")), "")
        ok.setFixedWidth(100)
        gui.password.setEchoMode(QLineEdit.Password)
        logo.setStyleSheet("QPushButton{background-color: '#318CE7';  border: 0px #318CE7;" "border-radius: 0px;}")
        gui.login.setStyleSheet("QLineEdit {background-color: '#95BEE7';  border: 0px #95BEE7;" "border-radius: 10px;}")
        gui.password.setStyleSheet("QLineEdit {background-color: '#95BEE7';  border: 0px #95BEE7;" "border-radius: 10px;}")
        ok.setStyleSheet("QPushButton {background-color: '#95BEE7';  border: 0px #95BEE7;" "border-radius: 10px;}")
        ok.clicked.connect(login)
        cansel.setStyleSheet("QPushButton {background-color: '#95BEE7';  border: 0px #95BEE7;" "border-radius: 10px;}")
        cansel.clicked.connect(gui.start)
        body.addWidget(logo)
        body.addWidget(gui.login)
        body.addWidget(gui.password)
        buttons.addStretch(1)
        buttons.addWidget(cansel)
        buttons.addWidget(ok)
        body.addLayout(buttons)
        preBody.setStyleSheet("QFrame{background-color: '#318CE7';  border: 2px #318CE7;" "border-radius: 7px;}")
        preBody.setLayout(body)
        layBody.addStretch(1)
        layBody.addWidget(preBody)
        layBody.addStretch(1)
        skelet.addLayout(layBody)
        skelet.addStretch(1)
        preSkelet.setLayout(skelet)
        gui.setCentralWidget(preSkelet)


if __name__ == "__main__":
    App = QtWidgets.QApplication([])
    os.environ["GIT_PYTHON_REFRESH"] = "quiet"
    import git

    st = guii()
    st.show()
    sys.exit(App.exec_())

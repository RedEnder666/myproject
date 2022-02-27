import json
import os
import requests as req
import re
import PyQt5
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor, QTextFormat
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
                             QMessageBox, QTextEdit)
from PyQt5 import uic, QtGui
import subprocess
import sys

token_folder = 'C:/Glow/data.tok'

def get_token():
    try:
        with open(token_folder, 'r') as f:
            return f.read()
    except Exception as e:
        print(e)
        return False

def write_token(token):
    try:
        with open(token_folder, 'w') as f:
            f.write(token)
    except Exception as e:
        print(e)
        os.mkdir('C:/Glow')
        open(token_folder, 'w').close()
        write_token(token)

def my_excepthook(type, value, traceback):
    print('Unhandled error:', type, value, traceback)

sys.excepthook = my_excepthook

def post(url, data):
    resp = req.post(url, json=data)
    return resp

def check_mail(mail):
    return re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mail)

def check_password(password):
    if len(password) < 8:
        return "Make sure your password is at lest 8 letters"
    elif re.search('[0-9]',password) is None:
        return "Make sure your password has a number in it"
    elif re.search('[A-Z]',password) is None:
        return "Make sure your password has a capital letter in it"
    else:
        return True


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ip = 'https://exilllite'
        self.reg = False
        try:
            self.token = get_token()
        except:
            self.token = None
        self.mouse_on_statusbar = False
        if not self.token:
            self.login_window()
        else:
            self.courses()

    def courses(self):
        self.load_ui('ui/menu.ui')

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.mouse_on_statusbar = event.y() < 30

    def mouseMoveEvent(self, event):
        if self.mouse_on_statusbar:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta .y())
            self.oldPos = event.globalPos()


    def login_window(self):
        self.load_ui('ui/login.ui')
        self.regButton.clicked.connect(self.register_window)
        self.loginButton.clicked.connect(self.login)
        print(os.environ)
        try:
            if os.environ["Glow_token"]:
                self.courses_window()

        except:
            pass

    def login(self):
        data = {'method': 'login', "email": self.mailEdit.text(), "password": self.passwordEdit.text(), 'stay': False}
        request = post(self.ip, data)
        if request.text != 'NO' or request.text != 'ERROR':
            self.token = request.text[3::]
            if self.stayCheck.isChecked():
                write_token(self.token)
            self.courses_window()




    def register_window(self):
        self.load_ui('ui/register.ui')
        self.loginButton.clicked.connect(self.login_window)
        self.regButton.clicked.connect(self.register)

    def register(self):
        data = {'method': 'reg', "name": self.nameEdit.text(), "surname": self.surnameEdit.text(),
                           "email": self.mailEdit.text(), "password": self.passwordEdit.text()}
        if not check_mail(data['email']):
            return 'Mail error'
        x = check_password(data['password'])
        if not x or self.passwordEdit.text() != self.passwordEdit_2.text():
            print(x if self.passwordEdit.text()  == self.passwordEdit_2.text() else "Non-equal")
            return x

        request = post(self.ip, data)


    def courses_window(self):
        self.load_ui('ui/menu.ui')
        self.courcesList.addItem('Тест')
        data = {'method': 'get_courses', 'token': self.token}
        request = post(self.ip, data)
        print(request.text)




    def load_ui(self, ui):
        '''for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()'''
        uic.loadUi(ui, self)
        try:
            self.exitButton.clicked.connect(sys.exit)
            self.minimizeButton.clicked.connect(self.showMinimized)
            self.setWindowFlags(Qt.FramelessWindowHint)
        except:
            pass
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = Main()
    sys.exit(app.exec_())
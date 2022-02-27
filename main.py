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
import os
import time
import sys

chat = eval(open('savedchat.dat', 'r', encoding='utf-8').read())
courses = eval(open('savedcourse.dat', 'r', encoding='utf-8').read())


def my_excepthook(type, value, traceback):
    print('Unhandled error:', type, value, traceback)

sys.excepthook = my_excepthook


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login()

    def login(self):
        self.load_ui('ui/login_demo.ui')
        self.tButton.clicked.connect(lambda: self.courses(True))
        self.sButton.clicked.connect(self.courses)
        self.chatButton.clicked.connect(self.chat)


    def chat(self):
        self.load_ui('ui/chat.ui')
        for i in chat:
            self.chatList.addItem(i)
        self.eButton.clicked.connect(self.message)
        self.bButton.clicked.connect(self.login)

    def message(self):
        chat.append(f"Имя Фамилия: {self.inputChat.text()}")
        self.chatList.addItem(f"Имя Фамилия: {self.inputChat.text()}")
        self.inputChat.setText('')


    def courses(self, teacher=False):
        self.course = None
        self.module = None
        self.load_ui('ui/teachers_demo.ui')
        for i in courses:
            self.cList.addItem(i)
        if teacher:
            self.cList.addItem('Добавить курс...')
        self.cList.itemClicked.connect(self.icClick)
        self.mList.itemClicked.connect(self.imClick)
        self.accButton.clicked.connect(self.login)


    def icClick(self, event):
        if event.text() == 'Добавить курс...':
            self.admin()
        else:
            self.course = event.text()
            self.coursesBox.setTitle(event.text())
            self.mList.clear()
            for i in courses[event.text()]:
                self.mList.addItem(i)

    def admin(self):
        self.load_ui('ui/coursemod_demo.ui')
        self.mList.itemClicked.connect(self.immClick)
        self.mList.itemDoubleClicked.connect(self.imm2Click)
        self.bButton.clicked.connect(lambda: self.courses(True))

    def immClick(self, event):
        if event.text() == "Добавить тему...":
            self.mList.insertItem(0, "Новая тема")
            for index in range(self.mList.count() - 1):
                item = self.mList.item(index)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def imm2Click(self, event):
        if event.text() != "Добавить тему...":
            event.setText('')

    def imClick(self, event):
        self.load_ui('ui/course_demo.ui')
        self.score.hide()
        self.courseName.setText(self.course)
        self.bButton.clicked.connect(self.courses)
        self.module = event.text()
        for i in courses[self.course][self.module]:
            self.tList.addItem(i)
        self.tList.itemClicked.connect(self.taskClick)

    def taskClick(self, event):
        self.score.show()
        for button in self.taskBox.findChildren(QWidget):
            button.deleteLater()
        self.taskBox.setTitle(event.text())
        # courses[self.course][self.module][event.text()]
        self.score.setValue(courses[self.course][self.module][event.text()]['value'])
        if courses[self.course][self.module][event.text()]['task'] == 0:
            self.taskText = QTextBrowser(self.taskBox)
            self.taskText.move(10, 20)
            self.taskText.show()
            self.taskText.resize(400, 345)
            self.taskText.setHtml(courses[self.course][self.module][event.text()]['description'])

            self.taskButton = QPushButton(self.taskBox)
            self.taskButton.move(400, 390)
            self.taskButton.resize(75, 20)
            self.taskButton.setText("Прочитал")
            self.taskButton.show()
            self.taskButton.clicked.connect(lambda: self.check(event))
        if courses[self.course][self.module][event.text()]['task'] == 1:
            self.taskText = QTextBrowser(self.taskBox)
            self.taskText.move(10, 20)
            self.taskText.show()
            self.taskText.resize(400, 155)
            self.taskText.setText(courses[self.course][self.module][event.text()]['description'])

            self.taskInput = QLineEdit(self.taskBox)
            self.taskInput.move(10, 195)
            self.taskInput.resize(250, 15)
            self.taskInput.setPlaceholderText('Ответ')
            self.taskInput.show()

            self.taskButton = QPushButton(self.taskBox)
            self.taskButton.move(400, 390)
            self.taskButton.resize(75, 20)
            self.taskButton.setText("Отправить")
            self.taskButton.show()
            self.taskButton.clicked.connect(lambda: self.check(event))

        print(courses[self.course][self.module][event.text()]['name'])


    def check(self, event):
        time.sleep(0.2)
        print(courses[self.course][self.module][event.text()]['task'])
        if courses[self.course][self.module][event.text()]['task'] == 1:
            score = 100 * (str(self.taskInput.text()) == str(courses[self.course][self.module][event.text()]['ans']))
        else:
            score = 100
        self.score.setValue(score)
        courses[self.course][self.module][event.text()]['value'] = score





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

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.mouse_on_statusbar = event.y() < 30

    def mouseMoveEvent(self, event):
        if self.mouse_on_statusbar:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = Main()
    sys.exit(app.exec_())
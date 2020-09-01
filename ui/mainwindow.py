# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confw.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


# import gettext
# gettext.textdomain("ubuntu-kylin-software-center")
# _ = gettext.gettext

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(520,370)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QFrame(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.centralwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget.setAttribute(Qt.WA_TranslucentBackground)
        self.centralwidget.setGeometry(QtCore.QRect(10, 10,500,350))

        self.centralwidget.setStyleSheet(".QWidget{background-color:#fafafa;border-radius:10px;}")
        self.windowwidget=QWidget(self.centralwidget)
        self.windowwidget.setObjectName(_fromUtf8("windowwidget"))
        self.windowwidget.setGeometry(QtCore.QRect(10, 10, 480, 330))

        self.title=QWidget(self.windowwidget)
        self.title.setObjectName(_fromUtf8("title"))
        self.title.setGeometry(QtCore.QRect(1, 1, 400, 30))
        self.title.setStyleSheet(".QWidget{background-color:#fafafa;}")

        self.title_icon=QLabel(self.title)
        self.title_icon.setObjectName(_fromUtf8("title_icon"))
        self.title_icon.setGeometry(QtCore.QRect(10, 1, 24, 24))
        self.title_icon.setStyleSheet(".QLabel{background-color:transparent;;background-image:url('res/logo.png');}")

        self.title_text=QLabel(self.title)
        self.title_text.setObjectName(_fromUtf8("title_text"))
        self.title_text.setGeometry(QtCore.QRect(45,1,200,24))
        self.title_text.setText("安装管理器")
        self.title_text.setStyleSheet("QLabel{font-size:16px;color:#444444;}")

        self.icon=QLabel(self.windowwidget)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.icon.setGeometry(QtCore.QRect(60, 114, 48, 48))
        self.icon.setStyleSheet(".QLabel{background-color:transparent;border:0px;border-radius:0px}")

        self.pkgname=QLabel(self.windowwidget) #软件包名label
        self.pkgname.setObjectName(_fromUtf8("pkgname"))
        self.pkgname.setGeometry(QtCore.QRect(123, 100, 270, 36))
        self.pkgname.setStyleSheet(".QLabel{background-color:transparent;border:0px;font-size:26px;color:#444444}")
        self.pkgname.setAlignment(Qt.AlignCenter)
        self.pathwidth = QFontMetrics(self.pkgname.font())
        # self.pkgname.setText("茄子摄像头")

        self.Version=QLabel(self.windowwidget)
        self.Version.setObjectName(_fromUtf8("pkgname"))
        self.Version.setGeometry(QtCore.QRect(123, 144, 270, 20))
        self.Version.setStyleSheet(".QLabel{background-color:transparent;border:0px;font-size:14px;color:#444444}")
        self.Version.setAlignment(Qt.AlignCenter)

        self.btnClose = QPushButton(self.windowwidget)
        self.btnClose.setGeometry(QtCore.QRect(440, 0, 38, 32))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.btnClose.setFocusPolicy(Qt.NoFocus)

        self.install=QPushButton(self.windowwidget)
        self.install.setObjectName(_fromUtf8("pkgname"))
        self.install.setGeometry(QtCore.QRect(165, 210, 150, 45))
        self.install.setStyleSheet("QPushButton{background-color:#2d8ae1;border:0px;font-size:16px;border-radius:4px;color:#ffffff}QPushButton:hover{background-color:#3580c4;border:0px;border-radius:4px;font-size:16px;color:#ffffff}")
        self.install.setText("快速安装")

        self.loding = QMovie("./res/loading1.gif")
        self.progressBar = QLabel(self.windowwidget)
        self.progressBar.setObjectName(_fromUtf8("btnClose"))
        self.progressBar.setGeometry(QtCore.QRect(65, 250, 350, 10))
        self.progressBar.setMovie(self.loding)
        # self.progressBar.setTextVisible(False)
        # self.progressBar.setVisible(False)
        self.progressBar.setStyleSheet("QProgressBar{background-color:#e5e5e5;}")

        self.status=QLabel(self.windowwidget)
        self.status.setObjectName(_fromUtf8("pkgname"))
        self.status.setGeometry(QtCore.QRect(210, 265, 80, 20))
        self.status.setStyleSheet(".QLabel{background-color:transparent;border:0px;font-size:14px;}")
        self.status.setText("正在安装...")
        self.status.hide()

        self.percent=QLabel(self.windowwidget)
        self.percent.setObjectName(_fromUtf8("pkgname"))
        self.percent.setGeometry(QtCore.QRect(264, 265, 40, 20))
        self.percent.setStyleSheet(".QLabel{background-color:transparent;border:0px;font-size:14px;}")
        self.percent.setText("99%")
        self.percent.hide()












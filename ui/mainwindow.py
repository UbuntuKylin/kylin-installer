# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confw.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import math

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

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        #取消button灰色背景
        self.palette = QPalette()
        self.ColorPlaceHolderText = QColor(255,255,255,0)
        self.brush = QBrush()
        self.brush.setColor(self.ColorPlaceHolderText)
        self.palette.setBrush(QPalette.Button, self.brush)
        self.palette.setBrush(QPalette.ButtonText, self.brush)

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(610,390)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)

        self.centralWidget=QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.centralWidget.setGeometry(QtCore.QRect(10, 10, 590, 370))

        self.message = QLabel(self.centralWidget)
        self.message.setObjectName(_fromUtf8("message"))
        self.message.setGeometry(95, 98, 400, 64)
        # self.message.setStyleSheet("QLabel{background-color:blue}")
        self.messageLayout = QHBoxLayout(self.message)
        self.buttonLayout = QHBoxLayout(self.centralWidget)

        self.title=QWidget(self.centralWidget)
        self.title.setObjectName(_fromUtf8("title"))
        self.title.setGeometry(QtCore.QRect(0, 0, 500, 36))
        # self.title.setStyleSheet(".QWidget{background-color:#fafafa;}")

        self.title_icon=QLabel(self.title)
        self.title_icon.setObjectName(_fromUtf8("title_icon"))
        self.title_icon.setGeometry(QtCore.QRect(15, 10, 24, 24))
        self.title_icon.setStyleSheet("QLabel{;background-image:url('res/logo.svg')}")

        self.title_text=QLabel(self.title)
        self.title_text.setObjectName(_fromUtf8("title_text"))
        self.title_text.setGeometry(QtCore.QRect(45,10,200,24))
        self.title_text.setText("麒麟应用安装器")
        self.title_text.setContentsMargins(0,0,0,0)
        self.title_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # self.title_text.setStyleSheet("QLabel{background-color:red}")
        self.title_text_ft = QFont()
        # self.title_text_ft.setBold(True)
        self.title_text_ft.setPixelSize(14)
        self.title_text_ft.setFamily("Microsoft YaHei")
        self.title_text.setFont(self.title_text_ft)
        # self.title_text.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        self.icon=QLabel(self.centralWidget)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.icon.setFixedSize(64, 64)

        self.tips=QLabel()
        self.tips.setObjectName(_fromUtf8("tips"))
        self.tips.setFixedSize(200, 64)
        self.tips.setContentsMargins(0,0,0,0)
        # self.tips.setStyleSheet("QLabel{background-color:blue}")
        self.pkgname=QLabel(self.tips) #软件包名label
        self.pkgname.setObjectName(_fromUtf8("pkgname"))
        self.pkgname.setContentsMargins(0,0,0,0)
        # self.pkgname.setStyleSheet("QLabel{background-color:red}")
        self.pkgname_ft = QFont()
        self.pkgname_ft.setFamily("Microsoft YaHei")
        self.pkgname_ft.setPixelSize(26)
        self.pkgname.setFont(self.pkgname_ft)
        self.pkgname.setGeometry(QtCore.QRect(0, 8, 200, 30))
        self.pkgname.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.pathwidth = QFontMetrics(self.pkgname.font())
        # self.pkgname.setText("茄子摄像头")

        #设置软件版本信息
        self.version=QLabel(self.tips)
        self.version.setObjectName(_fromUtf8("Version"))
        self.version.setGeometry(QtCore.QRect(0, 46, 200, 12))
        self.version.setContentsMargins(0,0,0,0)
        # self.version.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.version_ft = QFont()
        # self.version_ft.setBold(True)
        self.version_ft.setFamily("Microsoft YaHei")
        self.version_ft.setPixelSize(12)
        self.version.setFont(self.version_ft)
        # self.version.setStyleSheet(".QLabel{border:0px;font-size:12px;color:#444444;font-family:Microsoft YaHei}")
        # self.Version.setAlignment(Qt.AlignLeft)

        self.messageLayout.addStretch()
        self.messageLayout.addWidget(self.icon)
        self.messageLayout.addSpacing(15)
        self.messageLayout.addWidget(self.tips)
        self.messageLayout.addStretch()
        self.messageLayout.setContentsMargins(0,0,0,0)
        self.messageLayout.setSpacing(0)
        self.message.setLayout(self.messageLayout)

        # 菜单栏
        self.menuButton = QToolButton(self.centralWidget)
        self.menuButton.setGeometry(487, 5, 30, 30)
        self.menuButton.setIconSize(QSize(16,16))
        self.menuButton.setObjectName(_fromUtf8("menuButton"))
        self.menuButton.setIcon(QIcon.fromTheme("open-menu-symbolic"))
        self.menuButton.setFocusPolicy(Qt.NoFocus)
        self.menuButton.setPopupMode(QToolButton.InstantPopup) #未设置该属性会出现下拉箭头
        self.menuButton.setPalette(self.palette)
        self.menuButton.setProperty("useIconHighlightEffect", True)
        self.menuButton.setProperty("iconHighlightEffectMode", 1)
        # self.menuButton.hide()

        # 最小化按钮
        self.minButton = QPushButton(self.centralWidget)
        self.minButton.setGeometry(QtCore.QRect(521, 5, 30, 30))
        self.minButton.setIconSize(QSize(14,14))
        self.minButton.setObjectName(_fromUtf8("minButton"))
        # self.minButton.setIcon(QIcon.fromTheme("window-minimize-symbolic"))
        self.minButton.setFocusPolicy(Qt.NoFocus)
        self.minButton.setPalette(self.palette)
        self.minButton.setProperty("useIconHighlightEffect", True)
        self.minButton.setProperty("iconHighlightEffectMode", 1)

        # 关闭软件按钮
        self.closeButton = QPushButton(self.centralWidget)
        self.closeButton.setGeometry(QtCore.QRect(555, 5, 30, 30))
        self.closeButton.setIconSize(QSize(14,14))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        # self.closeButton.setIcon(QIcon.fromTheme("window-close-symbolic"))
        self.closeButton.setPalette(self.palette)
        self.closeButton.setProperty("useIconHighlightEffect", True)
        self.closeButton.setProperty("iconHighlightEffectMode", 1)
        # self.closeButton.setFlat(True)

        self.install=QPushButton(self.centralWidget)
        self.install.setObjectName(_fromUtf8("pkgname"))
        self.install.setGeometry(QtCore.QRect(220, 234, 150, 45))
        self.install.setStyleSheet("QPushButton{background-color:#2d8ae1;border:0px;font-size:16px;border-radius:4px;color:#ffffff}"
                                   "QPushButton:hover{background-color:#3580c4;border:0px;border-radius:4px;font-size:16px;color:#ffffff}")
        self.install.setText("一键安装")

        self.loding = QMovie("./res/loading1.gif")
        self.progressBar = QLabel(self.centralWidget)
        self.progressBar.setObjectName(_fromUtf8("closeButton"))
        self.progressBar.setGeometry(QtCore.QRect(120, 255, 350, 4))
        self.progressBar.setMovie(self.loding)
        # self.progressBar.setTextVisible(False)
        # self.progressBar.setVisible(False)
        self.progressBar.setStyleSheet("QProgressBar{background-color:#e5e5e5;}")

        self.status=QLabel(self.centralWidget)
        self.status.setObjectName(_fromUtf8("status"))
        self.status.setGeometry(QtCore.QRect(246, 274, 98, 24))
        self.status_ft=QFont()
        self.status_ft.setPixelSize(12)
        self.status_ft.setFamily("Microsoft YaHei")
        # self.status_ft.setBold(True)
        self.status.setFont(self.status_ft)
        # self.status.setStyleSheet(".QLabel{background-color:transparent;border:0px;font-size:12px;}")
        self.status.setText("正在安装...")
        self.status.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.status.hide()

        # 安装结束后的提示图标
        self.status_icon = QLabel(self.centralWidget)
        self.status_icon.setObjectName(_fromUtf8("status_icon"))
        self.status_icon.setGeometry(QtCore.QRect(186, 101, 48, 48))
        self.status_icon.hide()

        # 安装结束后的提示信息
        self.status_text = QLabel(self.centralWidget)
        self.status_text.setObjectName(_fromUtf8("status_text"))
        self.status_text.setGeometry(249, 107, 200, 47)
        self.status_text.setContentsMargins(0,0,0,2)
        # self.status_text.setStyleSheet("QLabel{background-color:red}")
        self.status_text.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.status_text.hide()

        self.status_text_ft = QFont()
        self.status_text_ft.setPixelSize(36)
        self.status_text_ft.setFamily("Microsoft YaHei")
        # self.status_text_ft.setBold(True)
        self.status_text.setFont(self.status_text_ft)
        # self.status_ft.set
        # 菜单栏
        self.menu = Menu(self.centralWidget)
        self.menuButton.setMenu(self.menu)

class Menu(QMenu):
    def __init__(self,parent):
        super(Menu, self).__init__(parent)
        self.group = QActionGroup(self)
        self.group.setExclusive(True)
        self.dark_model_action = self.addAction(str('深色模式'))
        self.dark_model_action.setCheckable(True)
        self.group.addAction(self.dark_model_action)
        self.white_model_action = self.addAction(str('浅色模式'))
        self.white_model_action.setCheckable(True)
        self.group.addAction(self.white_model_action)
        # self.help_action = self.addAction(str('帮助'))
        # self.help_action.setCheckable(True)
        # self.group.addAction(self.help_action)
        # self.abort_action = self.addAction(str('关于'))
        # self.abort_action.setCheckable(True)
        # self.group.addAction(self.abort_action)


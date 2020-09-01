#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE
import logging
import signal

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication
from ui.mainwindow import Ui_MainWindow
from backend.install_backend import InstallBackend
import math
from apt.debfile import DebPackage
from ui.config import File_window
from utils.debfile import DebFile
from utils import get_icon
from ui.messagebox import MessageBox
from ui.enums import AppActions
import fcntl
import gettext
_ = gettext.gettext
_homepath = os.path.expanduser("~")
LOG = logging.getLogger("install")
LAUNCH_MODE=''
REMOVE_SOFT=''
LOCAL_DEB_FILE=''

class  initThread(QThread):
    backend = None
    def __init__(self):
        super(initThread, self).__init__()
        self.backend = InstallBackend()

    def run(self):
        # init dbus backend
        self.backend.init_dbus_ifaces()

class workThread(QThread):
    def __init__(self, backend):
        super(workThread, self).__init__()
        self.backend = backend
    def run(self):
        try:
            self.backend.install_debfile(LOCAL_DEB_FILE)
        except Exception as e:
            print("install error: %s" % str(e))
            LOG.error(str(e))

class Example(QWidget):
    MAIN_WIDTH_NORMAL=500
    MAIN_HEIGHT_NORMAL=350
    resizeFlag =False
    def __init__(self):
        super(Example, self).__init__()
        # self.dbus_Thread = initThread()
        # self.dbus_Thread.start()
        # self.backend = self.dbus_Thread.backend
        self.backend = InstallBackend()
        self.backend.init_dbus_ifaces()
        self.InitUI()
        self.work = workThread(self.backend)
        self.messageBox = MessageBox(self)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.backend.dbus_apt_process.connect(self.slot_status_change)
        self.show_debfile(LOCAL_DEB_FILE)

    def InitUI(self):
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.paintEvent=self.set_paintEvent
        self.ui.icon.setStyleSheet(".QWidget{background-color:transparent;background-image:url('res/no-download.png');border:1px solid red;border-radius:0px}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}QPushButton:pressed{background-image:url('res/close-2.png');background-color:#bb3c3c;}")

    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.clickx = event.globalPos().x()
            self.clicky = event.globalPos().y()
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    #
    #函数名: 窗口拖动事件
    #Function: Window drag event
    #
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton):
            # resize
            if(self.resizeFlag == True):
                targetWidth = event.globalX() - self.frameGeometry().topLeft().x()
                targetHeight = event.globalY() - self.frameGeometry().topLeft().y()

                if(targetWidth < self.MAIN_HEIGHT_NORMAL):
                    if(targetHeight < self.MAIN_HEIGHT_NORMAL):
                        self.resize(self.MAIN_WIDTH_NORMAL, self.MAIN_HEIGHT_NORMAL)
                    else:
                        self.resize(self.MAIN_HEIGHT_NORMAL, targetHeight)
                else:
                    if(targetHeight < self.MAIN_HEIGHT_NORMAL):
                        self.resize(targetWidth, self.MAIN_HEIGHT_NORMAL)
                    else:
                        self.resize(targetWidth, targetHeight)

                event.accept()
            # drag move
            else:
                if(self.dragPosition != -1):
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()

    #
    #函数名：重绘窗口阴影
    #Function: Redraw window shadow
    #
    def set_paintEvent(self, event):
        painter=QPainter (self.ui.centralwidget)
        m_defaultBackgroundColor = QColor(qRgb(192,192,192))
        m_defaultBackgroundColor.setAlpha(50)
        path=QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(10, 10, self.ui.centralwidget.width() - 20, self.ui.centralwidget.height() - 20, 4, 4)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(QColor(m_defaultBackgroundColor.red(),
                                             m_defaultBackgroundColor.green(),
                                             m_defaultBackgroundColor.blue())))

        color=QColor(0, 0, 0, 20)
        i=0
        while i<4:
            path=QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRoundedRect(10 - i, 10 - i,self.ui.centralwidget.width() - (10 - i) * 2, self.ui.centralwidget.height() - (10 - i) * 2, 6, 6)
            color.setAlpha(100 - math.sqrt(i) * 50)
            painter.setPen(color)
            painter.drawPath(path)
            i=i+1

        painter.setRenderHint(QPainter.Antialiasing)

    #
    #函数：关闭软件&退出dbus
    #
    def slot_close(self):
        try:
            close_filelock()
            self.backend.exit()
            sys.exit(0)
        except Exception as e:
            print("kkk",e)

    #
    # 函数：安装软件
    #
    def install_debfile(self):
        #self.start_dpkg()
        self.work.start()

    #
    # 函数：显示软件包状态
    #
    def show_debfile(self,path):
        self.debfile = DebFile(path)
        self.ui.pkgname.setStyleSheet(".QLabel{background-color:transparent;border:0px;font-size:26px;color:#444444}")
        if path == '':
            # self.ui.pkgname.setText()
            text = get_icon.setLongTextToElideFormat(self.ui.pkgname, _("暂无可安装文件"))
        else:
            text = get_icon.setLongTextToElideFormat(self.ui.pkgname, _(str(self.debfile.name)))
            if str(text).endswith("…") is True:
                self.ui.pkgname.setToolTip(self.debfile.name)

        self.app = self.debfile
        iconpath = get_icon.get_icon_path(str(self.debfile.name))
        if iconpath:
            self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "');background-color:transparent;}")
        if self.debfile.version:
            text = get_icon.setLongTextToElideFormat(self.ui.Version, "版本号： " + self.debfile.version)
            if str(text).endswith("…") is True:
                self.ui.Version.setToolTip(self.debfile.version)

        else:
            self.ui.Version.setText("版本号：暂无")
        self.ui.install.clicked.connect(self.install_debfile)

    #
    # 函数：接收后台信号修改包状态
    #
    def slot_status_change(self, name, processtype, action, percent, msg):
        print(("####", name, " ", processtype, " ", action, " ", msg))
        if action == AppActions.INSTALLDEBFILE:
            if processtype == "apt" and percent < 0:
                self.stop_dpkg()
                self.ui.status.hide()
                self.ui.loding.stop()
                self.ui.progressBar.hide()
                self.messageBox.alert_msg("安装失败")
                self.ui.install.show()
                app.percent = 0
            elif processtype == "apt" and percent == 200:
                self.stop_dpkg()
                self.messageBox.alert_msg("安装完成")
                self.ui.install.setText("已安裝")
                self.ui.install.setStyleSheet("background-color:#999999")
                self.ui.install.setEnabled(False)
                app.percent = percent
            elif processtype == "cancel" and percent == 0:
                self.stop_dpkg()
            elif processtype == "ensure":
                self.start_dpkg()

    #
    # 函数：安装完成后，修改ui界面
    #
    def stop_dpkg(self):
        self.ui.loding.stop()
        self.ui.status.hide()
        self.ui.progressBar.hide()
        self.ui.install.show()

    #
    # 函数：开始安装后，修改ui界面
    #
    def start_dpkg(self):
        self.ui.status.show()
        self.ui.install.hide()
        self.ui.loding.start()
        self.ui.progressBar.show()


def check_local_deb_file(url):
    return os.path.isfile(url)

#
#函数名：单例
#
pidfile=0
def app_instance():
    global pidfile
    pidfile = open(os.path.realpath(__file__), "r")
    try:
        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        sys.exit(0)

#
# 函数：关闭文件锁
#
def close_filelock():
    try:
        fcntl.fcntl(pidfile, fcntl.LOCK_NB)
    except:
        LOG.error("can't not release file lock")

if __name__ == "__main__":
    app_instance()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    QApplication.setApplicationName("安装管理器")
    QApplication.setWindowIcon(QIcon("res/logo.png"))
    argn = len(sys.argv)
    if(argn == 1):
        LAUNCH_MODE = 'normal'
    elif(argn > 1):
        arg = sys.argv[1]
        if(arg == '-quiet'):
            LAUNCH_MODE = 'quiet'
        elif(arg == '-remove'):
            if(sys.argv[2]):
                LAUNCH_MODE = 'remove'
                REMOVE_SOFT = sys.argv[2]
            else:
                sys.exit(0)
        else:
            LAUNCH_MODE = 'manual'
            if(check_local_deb_file(arg)):
                LOCAL_DEB_FILE = arg
                try:
                    DebPackage(str(LOCAL_DEB_FILE))
                except:
                    MessageBox = File_window()
                    MessageBox.setText(_("Failed to open the file. The file format is not supported or the file is abnormal"))
                    MessageBox.exec()
                    sys.exit(0)
            else:
                sys.exit(0)
    ex = Example()
    ex.show()
    signal.signal(signal.SIGINT, lambda : close_filelock())
    signal.signal(signal.SIGTERM, lambda : close_filelock())
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    sys.exit(app.exec_())


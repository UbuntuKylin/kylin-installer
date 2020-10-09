#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE
import logging
import signal
import subprocess

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import os
import apt
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
gettext.bindtextdomain("kylin-installer",  "/usr/share/locale")
gettext.textdomain("kylin-installer")
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
#
# 类：安装或卸载线程
#
class workThread(QThread):
    def __init__(self, backend, model):
        super(workThread, self).__init__()
        self.backend = backend
        self.model = model
    def run(self):
        try:
            if self.model == 'install':
                self.backend.install_debfile(LOCAL_DEB_FILE)
            elif self.model == 'remove':
                # print("use remove")
                self.backend.remove(REMOVE_SOFT)
        except Exception as e:
            print("install error: %s" % str(e))
            LOG.error(str(e))

#
# 类：解析是否存在desktop文件的线程
#
class parseThread(QThread, QObject):
    parse_over = pyqtSignal(str)

    def __init__(self, pkgname):
        super(parseThread, self).__init__()
        self.pkgname = pkgname

    def run(self):
        exec_word = None
        self.desktop_path = "/usr/share/applications/" + self.pkgname + ".desktop"
        print("desktop_path:%s" % self.desktop_path)
        #判断是否存在同名的desktop文件
        if os.path.exists(self.desktop_path):
            setting = QSettings(self.desktop_path, QSettings.IniFormat)
            setting.beginGroup("Desktop Entry")
            exec_word = str(setting.value("Exec")).split(" ")[0]
        #不存在同名的desktop文件则进行deb包解析
        else:
            self.debfile = DebPackage(LOCAL_DEB_FILE)
            for desktop in self.debfile.filelist:
                if desktop.endswith(".desktop"):
                    print(desktop)
                    self.desktop = desktop
                    setting = QSettings("/" + self.desktop, QSettings.IniFormat)
                    setting.beginGroup("Desktop Entry")
                    exec_word = str(setting.value("Exec")).split(" ")[0]
        self.parse_over.emit(exec_word)

class Example(QWidget):
    MAIN_WIDTH_NORMAL=500
    MAIN_HEIGHT_NORMAL=350
    resizeFlag =False
    def __init__(self, model):
        super(Example, self).__init__()
        # self.dbus_Thread = initThread()
        # self.dbus_Thread.start()
        # self.backend = self.dbus_Thread.backend
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.backend = InstallBackend()
        self.backend.init_dbus_ifaces()
        self.InitUI()
        self.ukui_judge()
        self.work = workThread(self.backend, model)
        #self.messageBox = MessageBox(self)
        self.backend.dbus_apt_process.connect(self.slot_status_change)
        self.border_width = 8
        # self.setAttribute()

    def InitUI(self):
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        if LAUNCH_MODE == 'manual':
            self.show_softinfo(path=LOCAL_DEB_FILE)
        elif LAUNCH_MODE == 'remove':
            self.show_softinfo(softname=REMOVE_SOFT)
        else:
            self.show_softinfo()
        self.ui.minButton.clicked.connect(self.minisize_window)
        self.ui.menu.white_model_action.triggered.connect(self.set_white_model)
        self.ui.menu.dark_model_action.triggered.connect(self.set_dark_model)
        self.ui.closeButton.clicked.connect(self.slot_close)
        self.ui.closeButton.installEventFilter(self)
        if LAUNCH_MODE == "normal":
            self.ui.install.setEnabled(False)
            self.ui.install.setStyleSheet("QPushButton{background-color:#A9A9A9;border:0px;font-size:16px;border-radius:4px;color:#ffffff}")
            self.ui.icon.setStyleSheet("QLabel{background-image:url('res/kylin-installer-64.svg')}")
        # self.ui.centralwidget.paintEvent=self.set_paintEvent
        # self.ui.closeButton.setStyleSheet("QPushButton:hover{background-color:red}QPushButton:pressed{background-color:red;}")

    #
    # 函数：设置浅色主题
    #
    def set_white_model(self):
        app.setStyle("ukui-light")
        for widget in app.allWidgets():
            widget.repaint()
        # theme = QSettings()

    #
    # 函数：设置深色主题
    #
    def set_dark_model(self):
        app.setStyle("ukui-dark")
        for widget in app.allWidgets():
            widget.repaint()

    #
    # 函数：鼠标点击事件
    #
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
    
    def paintEvent(self, event):
        # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        opt = QStyleOption()
        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        # print(opt.palette.base().color())
        pat.fillPath(path, QBrush(opt.palette.base().color()))

        color = QColor(0, 0, 0, 50)

        for i in range(10):

            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
            # i_path.addRect(ref)
            if i == 0:
                # print("i:" + str(i))
                # opt = QStyleOption()
                # opt.initFrom(self)
                # p = QPainter(self)
                # p.setRenderHint(QPainter.Antialiasing)
                # p.setBrush(opt.palette.base().color())
                # p.setPen(Qt.transparent)
                # p.setPen(Qt.NoPen)
                # # p.drawRect(opt.rect)
                # p.drawRoundedRect(ref, 8, 8)
                # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
                pass
            else:
                i_path.addRoundedRect(ref, self.border_width, self.border_width)
                color.setAlpha(int(150 - i ** 0.5 * 50))
                pat.setPen(color)
                pat.drawPath(i_path)

        # 圆角
        # pat2 = QPainter(self)
        # pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        # pat2.setBrush(Qt.white)
        # pat2.setPen(Qt.transparent)
        #
        # rect = self.rect()
        # rect.setLeft(9)
        # rect.setTop(9)
        # rect.setWidth(rect.width() - 9)
        # rect.setHeight(rect.height() - 9)
        # pat2.drawRoundedRect(rect, 4, 4)

        # 主题
        ref = QRectF(10, 10 , self.width() - 20, self.height() - 20)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(opt.palette.base().color())
        p.setPen(Qt.transparent)
        p.setPen(Qt.NoPen)
        # p.drawRect(opt.rect)
        p.drawRoundedRect(ref, 8, 8)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    #
    # 函数：paintevent绘制阴影
    #
    # def paintEvent(self, event):
    #     print("llllllljjjjjjjj")
    #     p = QPainter(self)
    #     p.setRenderHint(QPainter.Antialiasing)
    #     rectPath = QPainterPath()
    #     rect = self.rect()
    #     rect.setLeft(6)
    #     rect.setTop(6)
    #     rect.setWidth(rect.width() - 6)
    #     rect.setHeight(rect.height() - 6)
    #     rectPath.addRoundedRect(rect,6,6)
    #     pixmap = QPixmap(self.rect().size())
    #     pixmap.fill(Qt.transparent)
    #     pixmapPainter = QPainter(pixmap)
    #     pixmapPainter.setRenderHint(QPainter.Antialiasing)
    #     pixmapPainter.setPen(Qt.transparent)
    #     pixmapPainter.setBrush(Qt.black)
    #     pixmapPainter.drawPath(rectPath)
    #     pixmapPainter.end()
    #
    #     img = pixmap.toImage()
    #
    #     pixmap = QPixmap.fromImage(img)
    #     pixmapPainter2 = QPainter(pixmap)
    #     pixmapPainter2.setRenderHint(QPainter.Antialiasing)
    #     pixmapPainter2.setCompositionMode(QPainter.CompositionMode_Clear)
    #     pixmapPainter2.setPen(Qt.transparent)
    #     pixmapPainter2.setBrush(Qt.transparent)
    #     pixmapPainter2.drawPath(rectPath)
    #
    #     p.drawPixmap(self.rect(), pixmap, pixmap.rect())
    #
    #     opt = QStyleOption()
    #
    #     p.save()
    #     p.fillPath(rectPath, opt.palette.color(QPalette.Base))
    #     p.restore()
    #
    #函数：关闭软件&退出dbus
    #
    def slot_close(self):
        try:
            close_filelock()
            self.backend.exit()
            try:
                fcntl.flock(pidfile, fcntl.LOCK_UN)
            except:
                print("fcntl-error:close pidfile is failed!")
            sys.exit(0)
        except Exception as e:
            print("kkk",e)

    #
    # 函數：卸载软件
    #
    def remove(self):
        self.work.start()

    #
    # 函数：安装软件
    #
    def install_debfile(self):
        #self.start_install()
        self.work.start()

    #
    # 函数：显示软件包信息
    #
    def show_softinfo(self,path=None,softname=None):
        if path != None:
            self.debfile = DebFile(path)
            self.pkgname = self.debfile.name
            text = get_icon.setLongTextToElideFormat(self.ui.version, _("version：") + self.debfile.version)
            if str(text).endswith("…") is True:
                self.ui.version.setToolTip(self.debfile.version)
            self.parse = parseThread(self.pkgname)
            self.parse.parse_over.connect(self.parse_desktop)
            self.exec_word = None
        elif softname != None:
            self.cache = apt.Cache()
            pkg = self.cache[softname]
            self.pkg_name = pkg.shortname
            self.pkg_version = pkg.versions.keys()[0]
        if LAUNCH_MODE == 'normal':
            # self.ui.pkgname.setText()
            self.ui.install.setText(_("installation"))
            text = get_icon.setLongTextToElideFormat(self.ui.pkgname, _("select an installation file"))
            if str(text).endswith("…") is True:
                self.ui.pkgname.setToolTip(_("select an installation file"))
            self.ui.version.setText(_("version：no"))
        elif LAUNCH_MODE == 'manual':
            self.ui.install.setText(_("installation"))
            self.ui.install.clicked.connect(self.install_debfile)
            iconpath = get_icon.get_icon_path(str(self.debfile.name))
            text = get_icon.setLongTextToElideFormat(self.ui.pkgname, _(str(self.debfile.name)))  # 判断字符是否过长，自动生成省略号
            if str(text).endswith("…") is True:
                self.ui.pkgname.setToolTip(self.debfile.name)
            if iconpath:
                self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "');background-color:transparent;background-position:center;background-repeat:none}")
        elif LAUNCH_MODE == 'remove':
            if pkg.is_installed:
                self.ui.install.setText(_("uninstallation"))
                self.ui.install.clicked.connect(self.remove)
                self.ui.version.setText(_("version：") + self.pkg_version)
                iconpath = get_icon.get_icon_path(str(self.pkg_name))
                text = get_icon.setLongTextToElideFormat(self.ui.pkgname, _(self.pkg_name))  # 判断字符是否过长，自动生成省略号
                if str(text).endswith("…") is True:
                    self.ui.pkgname.setToolTip(self.pkg_name)
                if iconpath:
                    self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "');background-color:transparent;background-position:center;background-repeat:none}")
            else: #软件未安装时，提示信息
                self.ui.install.setText(_("uninstalled"))
                self.ui.install.setStyleSheet("QPushButton{background-color:#A9A9A9;border:0px;font-size:16px;border-radius:4px;color:#ffffff}")
                self.ui.install.setEnabled(False)
                text = get_icon.setLongTextToElideFormat(self.ui.pkgname, _("software not installed"))
                if str(text).endswith("…") is True:
                    self.ui.pkgname.setToolTip("software not installed")
                self.ui.version.setText(_("version：no"))
                iconpath = get_icon.get_icon_path(self.pkg_version)
                if iconpath:
                    self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "');background-color:transparent;background-position:center;background-repeat:none}")

    #
    # 函数：接收后台信号修改包状态
    #
    def slot_status_change(self, name, processtype, action, percent, msg):
        print(("####", name, " ", processtype, " ", action, " ", msg))
        if action == AppActions.INSTALLDEBFILE:
            if processtype == "apt" and percent < 0:
                self.stop_install(percent)
            elif processtype == "apt" and percent == 200:
                print("install over")
                self.stop_install(percent)
            elif processtype == "cancel" and percent == 0:
                # self.stop_install()
                pass
            elif processtype == "ensure":
                self.start_install()
        elif action == AppActions.REMOVE:
            if processtype == "apt" and percent < 0:
                self.stop_remove(percent)
            if processtype == "apt" and percent == 200:
                self.stop_remove(percent)
            elif processtype == "cancel" and percent == 0:
                # self.stop_remove()
                pass
            elif processtype == "ensure":
                self.start_remove()

    #
    # 函数：安装完成后解析desktop文件
    #
    def parse_desktop(self, exec_word):
        self.exec_word = exec_word
        if self.exec_word != "":
            self.ui.status_text.setText(_("installation is complete！"))
            self.ui.install.setText(_("experience"))
            self.ui.install.setEnabled(True)
            self.ui.install.clicked.connect(self.experience)
            self.ui.install.clicked.disconnect(self.install_debfile)
        else:
            self.ui.status_text.setText(_("installation is complete！"))
            self.ui.install.setText(_("installed"))
            self.ui.install.setEnabled(False)
        self.ui.status_icon.setStyleSheet("QLabel{background-image:url('res/success.png')}")
        self.ui.loding.stop()
        self.ui.status.hide()
        self.ui.pkgname.hide()
        self.ui.version.hide()
        self.ui.progressBar.hide()
        self.ui.install.move(220,229)
        self.ui.install.show()
        self.ui.icon.hide()
        self.ui.status_text.setFont(self.ui.status_text_ft)
        self.ui.status_text.show()
        self.ui.status_icon.show()

    #
    # 函数：立即体验安装完成后的软件
    #
    def experience(self):
        subprocess.Popen(self.exec_word)

    #
    # 函数：开始安装后，修改ui界面
    #
    def start_install(self):
        self.ui.status.setText(_("installing..."))
        self.ui.status.show()
        self.ui.install.hide()
        self.ui.loding.start()
        self.ui.progressBar.show()

    #
    # 函数：安装完成后，修改ui界面
    #
    def stop_install(self, percent):
        if percent > 0:
            self.parse.start()
            return
        else:
            self.ui.status_text.setText(_("Installation failed"))
            self.ui.install.setText(_("failed"))
            self.ui.status_icon.setStyleSheet("QLabel{background-image:url('res/error.png')}")
            self.ui.install.setEnabled(False)
            self.ui.install.setStyleSheet("QPushButton{background-color:#ffffff")
        self.ui.loding.stop()
        self.ui.status.hide()
        self.ui.pkgname.hide()
        self.ui.version.hide()
        self.ui.progressBar.hide()
        self.ui.install.move(220,229)
        self.ui.install.show()
        self.ui.icon.hide()
        self.ui.status_text.setFont(self.ui.status_text_ft)
        self.ui.status_text.show()
        self.ui.status_icon.show()

    #
    # 函数：开始卸载后，修改UI界面
    #
    def start_remove(self):
        self.ui.status.setText(_("uninstalling..."))
        self.ui.status.show()
        self.ui.install.hide()
        self.ui.loding.start()
        self.ui.progressBar.show()

    #
    # 函数：卸载完成后，修改UI界面
    #
    def stop_remove(self, percent):
        if percent > 0:
            # self.messageBox.alert_msg("安装完成")
            self.ui.install.setText(_("removed"))
            self.ui.status_text.setText(_("uninstall complete！"))
            # self.ui.install.setStyleSheet("background-color:#999999")
            self.ui.install.setEnabled(False)
            self.ui.status_icon.setStyleSheet("QLabel{background-image:url('res/success.png')}")
        else:
            self.ui.install.setText(_("failed"))
            self.ui.status_text.setText(_("uninstall failed！"))
            self.ui.install.setEnabled(False)
            self.ui.status_icon.setStyleSheet("QLabel{background-image:url('res/error.png')}")
        self.ui.loding.stop()
        self.ui.status.hide()
        self.ui.pkgname.hide()
        self.ui.version.hide()
        self.ui.progressBar.hide()
        self.ui.install.move(220, 229)
        self.ui.install.show()
        self.ui.icon.hide()
        self.ui.status_text.setFont(self.ui.status_text_ft)
        self.ui.status_text.show()
        self.ui.status_icon.show()

    #
    # 函数：过滤事件，设置关闭按钮状态
    #
    def eventFilter(self, watched, event):
        if str(os.getenv("QT_QPA_PLATFORMTHEME")) == "ukui":
            if watched == self.ui.closeButton:
                if event.type() == QEvent.Enter:
                    # self.ui.closeButton.setFlat(True)
                    self.ui.closeButton.setStyleSheet("QPushButton:hover{background-color:#F86457; border:0px; border-radius:4px}"
                                                      "QPushButton:click{background-color:#E44C50; border:0px; border-radius:4px}")
                elif event.type() == QEvent.Leave:
                    self.ui.closeButton.setIcon(QIcon.fromTheme("window-close-symbolic"))
                    self.ui.closeButton.setPalette(self.ui.palette)
                    self.ui.closeButton.setProperty("useIconHighlightEffect", True)
                    self.ui.closeButton.setProperty("iconHighlightEffectMode", 1)
            else:
                return

            # if event.type() == QEvent.Enter:
            #     self.ui.minButton.setFlat(True)
        return QWidget.eventFilter(self, watched, event)

    #
    # 函数：最小化窗口
    #
    def minisize_window(self):
        self.showMinimized()

    #
    # 函数：做ukui的主题判断，不存在则进行额外处理操作
    #
    def ukui_judge(self):
        if str(os.getenv("QT_QPA_PLATFORMTHEME")) == "ukui" :
            self.ui.closeButton.setIcon(QIcon.fromTheme("window-close-symbolic"))
            self.ui.minButton.setIcon(QIcon.fromTheme("window-minimize-symbolic"))
        else:
            self.ui.closeButton.setStyleSheet("QPushButton{border:none;background-image:url('res/window-close-symbolic.svg');background-position:center;background-repeat:none}"
                                              "QPushButton:hover{background-color:#E44C50}"
                                              "QPushButton:click{backgorund-color:#E44C50}")
            self.ui.minButton.setStyleSheet("QPushButton{border:none;background-image:url('res/window-minimize-symbolic.svg');background-position:center;background-repeat:none}"
                                            "QPushButton:hover{background-color:#DCDCDC}"
                                            "QPushButton:click{background-color:#DCDCDC}")
            self.ui.menuButton.hide()

    #
    # 右键任务栏图标点击关闭触发
    #
    def closeEvent(self, event):
        print("close")
        self.slot_close()

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
    QApplication.setApplicationName("麒麟应用安装器")
    QApplication.setWindowIcon(QIcon("res/kylin-installer-64.svg"))
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
    if LAUNCH_MODE == 'manual':
        print("manul")
        ex = Example('install')
    elif LAUNCH_MODE == 'remove':
        print("remove")
        ex = Example('remove')
    else:
        print("normal")
        ex = Example('normal')
    ex.show()
    signal.signal(signal.SIGINT, lambda : close_filelock())
    signal.signal(signal.SIGTERM, lambda : close_filelock())
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    sys.exit(app.exec_())


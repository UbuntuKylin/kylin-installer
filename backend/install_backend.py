#!/usr/bin/python3
# -*- coding: utf-8 -*

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:     
#     maclin <majun@ubuntukylin.com>
# Maintainer:
#     maclin <majun@ubuntukylin.com>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

### END LICENSE
import random

import dbus
import os
import shutil
import locale

import logging

from PyQt5.QtCore import *
from xdg import BaseDirectory as xdg
from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)

import gettext
gettext.textdomain("kylin-installer")
_ = gettext.gettext

LOG = logging.getLogger("uksc")
DBUS_SERVICE_PATH = "com.kylin.packages.manager.tools"
DBUS_INTERFACE_PATH = "com.kylin.packages.manager.tools"
INSTALLDEPS = "install_deps"
INSTALLDEBFILE = "install_debfile"
REMOVE = "remove"
CACHE_PATH = os.path.join(xdg.xdg_cache_home, "kylin-installer/debfile/*.deb")

AptActionMsg = {
    "install_deps":_("Install dependencies"),
    "install_debfile":_("Install local package"),
    "install":_("Software Installation"),
    "remove":_("Software uninstall"),
    "upgrade":_("Software upgrade"),
    "update":_("Source update"),
    "update_first":_("Source initialization"),
    "insdep":_("Install dependency")
}
AptProcessMsg = {
    "apt_start":_("Start..."),
    "apt_finish":_("Perfection!"),
    "apt_error":_("Failure!"),
    "apt_pulse":_("Processing"),
    "down_start":_("Download begins"),
    "down_stop":_("Download stopped"),
    "down_done":_("Download completed"),
    "down_fail":_("download failed"),
    "down_fetch":_("Single download completed"),
    "down_pulse":_("Download in progress"),
    "down_cancel":_("Download canceled"),
}

class InstallBackend(QObject):

    dbus_apt_process = pyqtSignal(str,str,str,int,str)
    init_models_ready = pyqtSignal(str, str)

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")

        self.iface = None

    #
    # 函数：初始化dbus接口
    #
    def init_dbus_ifaces(self):
        try:
            bus = dbus.SystemBus(mainloop)
        except Exception as e:
            return False
        try:
            obj = bus.get_object(DBUS_SERVICE_PATH,'/')
            self.iface = dbus.Interface(obj, dbus_interface=DBUS_INTERFACE_PATH)
            self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal)
            self.iface.connect_to_signal("software_auth_signal",self._on_software_auth_signal)
            self.rm_cache_pkgs(CACHE_PATH)
        except dbus.DBusException as e:
            LOG.error("dbus exception:%s" % str(e))
            return False
        return True

    #call the dbus functions by function name
    def call_dbus_iface(self, funcname, kwargs=None):
        if self.iface is None:
            return None

        func = getattr(self.iface,funcname)
        if func is None:
            return None

        res = None
        try:
            res = func(kwargs)
        except dbus.DBusException as e:
            return None

        return res

    #
    # 函数：退出dbus
    #
    def exit(self):
        self.call_dbus_iface('exit')

    #
    # 函数：删除用户目录下缓存的包
    #
    def rm_cache_pkgs(self, path):
        self.call_dbus_iface("rm_cache_pkgs", path)
    #
    # 函数：安装多个deb包调用
    #
    def install_deps(self, path):
        return self.call_dbus_iface(INSTALLDEPS, path)

    #
    # 函数：安装本地deb包
    #
    def install_debfile(self, path):
        debcache_dir = os.path.join(os.path.expanduser("~"), ".cache", "kylin-installer", "debfile")
        if (os.path.exists(debcache_dir) == False):
            os.makedirs(debcache_dir)
        for char in path:
            if u'\u4e00' <= char <= u'\u9fa5':  #判断路径是否存在中文
                filename = self.random_char(10)  #修改包名的为非中文
                debcache_path = os.path.join(debcache_dir, filename+".deb")
                shutil.copy(path, debcache_path)
                return self.call_dbus_iface(INSTALLDEBFILE, debcache_path)
        return self.call_dbus_iface(INSTALLDEBFILE, path)

    #
    # 函数：卸载软件包
    #
    def remove(self, pkgname):
        return self.call_dbus_iface(REMOVE, pkgname)

    #
    # 函数：生成随机字符串
    #
    def random_char(self, num):
        charlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        character = ''
        for i in range(num):
            character += random.choice(charlist)
        return character

    #
    # 函数：apt调用的返回信号响应
    #
    def _on_software_apt_signal(self,type, kwarg):
        sendType = "apt"
        appname = str(kwarg['apt_appname'])
        sendMsg  = ""
        percent = float(str(kwarg['apt_percent']))
        action = str(kwarg['action'])
        sendMsg = AptActionMsg[action] + AptProcessMsg[str(type)]
        # print("send over")
        self.dbus_apt_process.emit(appname,sendType,action,percent,sendMsg)

    #
    # 函数：auth信号响应
    #
    def _on_software_auth_signal(self,type, kwarg):
        sendType = "auth"
        appname = str(kwarg['appname'])
        #sendMsg  = "操作取消"
        action = str(kwarg['action'])
        if type == "auth_cancel":
            sendType = "cancel"
            sendMsg = _("Operation canceled")
        elif type == "auth_ensure":
            sendType = "ensure"
            sendMsg = _("Operation ensure")
        # print("type :%s" % type)
        self.dbus_apt_process.emit(appname,sendType,action,0,sendMsg)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     lijiang <lijiang@kylinos.cn>
# Maintainer:
#     lijiang <lijiang@kylinos.cn>

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

import sys
import os
import logging

import apt
import dbus
import dbus.service
import dbus.mainloop.glib
from apt.debfile import DebPackage
from kylin_packages_manager_tools_daemon.apt_daemon import AppActions, AptProcess
from gi.repository import GObject


log = logging.getLogger('PackagesManager')

INTERFACE = 'com.kylin.packages.manager.tools'
PACKAGES_MANAGER_TOOLS = 'com.kylin.packages.manager.tools.action'
UKPATH = '/'

class WorkitemError(Exception):

    def __init__(self, errornum, details = ""):
        self.errornum = errornum
        self.details = details

class PackagesManagerDbusService(dbus.service.Object):

    def __init__ (self, bus, mainloop):
        self.cache = apt.Cache()
        self.bus = bus
        self.bus_name = dbus.service.BusName(INTERFACE, bus=bus)
#        print "SoftwarecenterDbusService:",self.bus_name
        dbus.service.Object.__init__(self, self.bus_name, UKPATH)
        self.mainloop = mainloop

    #
    # 函数：操作policykit提权
    #
    def auth_with_policykit(self, sender, action, text="要安装或卸载软件"):
        if not sender:
            raise ValueError('sender == None')

#        print "auth_with_policykit:", sender
        granted = False
        try:
            obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1',
                                                    '/org/freedesktop/PolicyKit1/Authority')
            policykit = dbus.Interface(obj, 'org.freedesktop.PolicyKit1.Authority')

            subject = ('system-bus-name', {'name': sender})
            flags = dbus.UInt32(1)   # AllowUserInteraction flag
            msg = text + "，您需要进行验证。"
            details = { 'polkit.message' : msg}
            cancel_id = '' # No cancellation id
            (granted, notused, details) = policykit.CheckAuthorization(
                            subject, action, details, flags, cancel_id)
        except Exception as e:
            print("error: %s" % str(e))
            print("auth with except......")
            granted = False

        return granted

    #
    # 函数：根据软件包获取软件名
    #
    def get_pkg_by_name(self, pkgName):
        #        print pkgName
        try:
            pkg = self.cache[pkgName]
        except KeyError:
            raise WorkitemError(1, "Package %s is not  available" % pkgName)
        else:
            if pkg.candidate is None:
                raise WorkitemError(1, "Package %s is not  available" % pkgName)
            else:
                return pkg
    #
    # 函数：安装软件包
    #
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def install_debfile(self, path, sender=None):
        print("####install deb file: ", path)
        # path = "".join([chr(character) for character in path]) # add by zhangxin for chinese .deb path 11.19
        # 开启密码认证机制
        granted = self.auth_with_policykit(sender, PACKAGES_MANAGER_TOOLS)
        if not granted:
            kwarg = {"appname": path,
                     "action": AppActions.INSTALLDEBFILE,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False
        else:
            kwarg = {"appname": path,
                     "action": AppActions.INSTALLDEBFILE,
                     }
            self.software_auth_signal("auth_ensure", kwarg)
            #print("send auth signal")
        if not os.path.isfile(path):
            raise WorkitemError(4, "%s is unreadable file" % path)
        try:
            debfile = DebPackage(path)
        except IOError:
            raise WorkitemError(4, "%s is unreadable file" % path)
        except Exception as e:
            raise WorkitemError(5, e)
        #self.cache.open()
        #获取软件包名
        pkgName = debfile._sections["Package"]
        debfile.check() #do debfile.check for the next to do debfile.missing_deps
        if 0 == len(debfile.missing_deps):
            # 安装软件包
            res = debfile.install()
            if res:
                kwarg = {"apt_appname": pkgName,
                         "apt_percent": str(-200),
                         "action": str(AppActions.INSTALLDEBFILE),
                         }
                self.software_apt_signal("apt_finish", kwarg)
                raise WorkitemError(6, "package manager failed")
            else:
                kwarg = {"apt_appname":pkgName,
                         "apt_percent":str(200),
                         "action":str(AppActions.INSTALLDEBFILE),
                         }
                self.software_apt_signal("apt_finish", kwarg)
        else:
            raise WorkitemError(16, "dependence not be satisfied")
        return True

    #
    # 函数：卸载软件包
    #
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def remove(self, pkgName, sender=None):
        print("####remove: ", pkgName)
        # 开启密码认证
        granted = self.auth_with_policykit(sender, PACKAGES_MANAGER_TOOLS)
        if not granted:
            kwarg = {"appname": pkgName,
                     "action": AppActions.REMOVE,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False
        self.cache.open()
        pkg = self.get_pkg_by_name(pkgName)
        if pkg.is_installed is False:
            raise WorkitemError(11, "Package %s isn't installed" % pkgName)
        pkg.mark_delete()

        try:
            self.cache.commit(None, AptProcess(self.dbus_service, pkgName, AppActions.REMOVE))
        except apt.cache.LockFailedException:
            raise WorkitemError(3, "package manager is running.")
        except Exception as e:
            raise WorkitemError(12, e)
        print("####remove return")
        return True

    #
    # 函数：退出dbus
    #
    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()
        sys.exit(0)

    #
    # 信号：发送认证信号
    #
    @dbus.service.signal(INTERFACE, signature='sa{ss}')
    def software_apt_signal(self, type, msg):
        pass

    @dbus.service.signal(INTERFACE, signature='sa{ss}')
    def software_auth_signal(self, type, msg):
        pass
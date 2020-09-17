import apt
import os
import aptsources.sourceslist
import apt.progress.base as apb
from apt.debfile import DebPackage
from apt.cache import FetchFailedException
import socket

class AppActions:
    INSTALLDEPS = "install_deps"
    INSTALLDEBFILE = "install_debfile"
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    CANCEL = "cancel"
    APPLY = "apply_changes"
    PURCHASE = "purchase"
    UPDATE = "update"

class AptProcess(apb.InstallProgress):
    '''Apt progress'''
    def __init__(self, dbus_service, appname, action):
        apb.InstallProgress.__init__(self)
        self.dbus_service = dbus_service
        self.appname = appname
        self.percent = 0
        self.action = action

    def conffile(self, current, new):
#        print 'there is a conffile question'
        pass

    def error(self, pkg, errormsg):
#        print "AptProcess, error:", self.appname, pkg, errormsg
        global FLAG
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(self.percent),
                 "action":str(self.action),
                 }
        self.dbus_service.set_uksc_not_working()
        if FLAG:
            self.dbus_service.software_apt_signal("apt_error", kwarg)
        else:
            FLAG =1

    def start_update(self):
#        print 'apt process start work', self.appname
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(self.percent),
                 "action":str(self.action),
                 }
        if(self.action == AppActions.INSTALLDEBFILE):
            kwarg["apt_percent"] = "50"
        if FLAG:
            self.dbus_service.software_apt_signal("apt_start", kwarg)

    def finish_update(self):
        global FLAG
#        print 'apt process finished', self.appname
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(200),
                 "action":str(self.action),
                 }
        if FLAG:
            self.dbus_service.software_apt_signal("apt_finish", kwarg)
        else:
            FLAG = 1
        #if self.appname == "kylin-software-center" and self.action == "upgrade":
        #    pass
        #else:
        self.dbus_service.set_uksc_not_working()

    def status_change(self, pkg, percent, status):
#        print "status_change:", self.appname, pkg
#        print str(int(percent)) + "%  status : " + status
#        self.percent = percent
#        if percent != self.percent:
#            print "&&&&&&&&&&&&&&&&&&&:",self.percent
        kwarg = {"apt_appname":str(self.appname),
#                 "install_percent":self.percent,
                 "apt_percent":str(percent),
                 "status":str(status),
                 "action":str(self.action),
                 }

#        print "####status_change:", kwarg
        if FLAG:
            self.dbus_service.software_apt_signal("apt_pulse", kwarg)
#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>

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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext


class File_window(QMessageBox):

    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)
        #self.setWindowTitle("软件源更新提示")
        # self.setWindowTitle(_("提示"))
        self.setWindowTitle(_("Tips"))
        # self.button_update = self.addButton(self.tr(_("确定")), QMessageBox.ActionRole)
        self.button_update = self.addButton(self.tr(_("determine")), QMessageBox.ActionRole)
        self.button_exit = self.addButton(self.tr(_("Quit")), QMessageBox.ActionRole)
        self.button_exit.hide()
        self.setEscapeButton(self.button_exit)


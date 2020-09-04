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

import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from xdg import BaseDirectory as xdg
UBUNTUKYLIN_DATA_PATH = (os.path.abspath(os.path.curdir) + "/data/")
UKSC_CACHE_DIR = os.path.join(xdg.xdg_cache_home, "uksc")
UBUNTUKYLIN_CACHE_ICON_PATH = os.path.join(UKSC_CACHE_DIR, "icons/")
UBUNTUKYLIN_RES_ICON_PATH = UBUNTUKYLIN_DATA_PATH + "icons/"
KYLIN_SYSTEM_ICON_48_PATH = "/usr/share/icons/kylin-icon-theme/48x48/apps/"
UK_SYSTEM_ICON_48_PATH = "/usr/share/icons/ukui-icon-theme-default/48x48/apps/"
DEBFILE_ICON_PATH="/usr/share/ubuntu-kylin-software-center/data/icons/"

def get_icon_path(app_name):
    iconPathList=[
        KYLIN_SYSTEM_ICON_48_PATH,
        UK_SYSTEM_ICON_48_PATH,
        UBUNTUKYLIN_CACHE_ICON_PATH,
        UBUNTUKYLIN_RES_ICON_PATH,
        DEBFILE_ICON_PATH
    ]
    extList=['.png','.jpg']
    for iconPath in iconPathList:
        for ext in extList:
            filePath=os.path.join(iconPath,str(app_name) + ext)
            if(os.path.isfile(filePath)):
                return filePath
    return os.path.join(UBUNTUKYLIN_RES_ICON_PATH,"default.png")

# add by kobe to format long text
def setLongTextToElideFormat(label, text):
    if text[len(text) - 1] == '\n':
        text = text.rstrip()
    metrics = QFontMetrics(label.font())
    elidedText = metrics.elidedText(text, Qt.ElideRight, label.width()-160)
    label.setText(elidedText)
    return elidedText

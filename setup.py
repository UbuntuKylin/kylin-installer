#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
from setuptools import setup
import DistUtilsExtra.command.build_extra
import DistUtilsExtra.command.build_i18n
import DistUtilsExtra.command.clean_i18n
from subprocess import call

PO_DIR = "po"
for po in glob.glob(os.path.join(PO_DIR, '*.po')):
    lang = os.path.basename(po[:-3])
    mo = os.path.join(PO_DIR, 'kylin-installer.mo')
    target_dir = os.path.dirname(mo)
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    try:
        return_code = call(['msgfmt', '-o', mo, po])
    except OSError:
        print('Translation not available, please install gettext')
        break
    if return_code:
        raise Warning('Error when building locales')


cmdclass ={
            "build" : DistUtilsExtra.command.build_extra.build_extra,
            "build_i18n" :  DistUtilsExtra.command.build_i18n.build_i18n,
            "clean": DistUtilsExtra.command.clean_i18n.clean_i18n,
}
data_files=[
    ('bin/', ['kylin-installer']),
    ('../etc/dbus-1/system.d/', ['backend/conf/com.kylin.packages.manager.tools.conf']),
    ('share/polkit-1/actions/', ['backend/conf/com.kylin.packages.manager.tools.policy']),
    ('share/dbus-1/system-services/', ['backend/conf/com.kylin.packages.manager.tools.service']),
    ('share/applications/',['kylin-installer.desktop']),
    ('share/icons/hicolor/scalable/apps',['kylin-installer.svg']),
    ('share/kylin-installer/data/icons/', glob.glob('data/icons/*.png')),
    ('share/kylin-installer/ui/', glob.glob('ui/*')),
    ('share/kylin-installer/utils/', glob.glob('utils/*')),
    ('share/kylin-installer/',['kylin-installer.py']),
    ('share/kylin-installer/backend/',glob.glob('backend/*.py')),
    ('share/kylin-installer/res/',glob.glob('res/*'))
    # ('../etc/xdg/autostart/',['kylin-installer.desktop']),
    ]

def find_mo_files():
    data_files = []
    for mo in glob.glob(os.path.join(PO_DIR, '*', 'ubuntu-kylin-software-center.mo')):
        dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
        data_files.append((dest, [mo]))
    return data_files

data_files.extend(find_mo_files())

setup(name="kylin-installer",
    version="1.3.10",
    author="Ubuntu Kylin Team",
    author_email="dengnan@kylinos.cn",
    url="https://launchpad.net/kylin-installer",
    license="GNU General Public License (GPL)",
    packages = [ 'kylin_packages_manager_tools_daemon',],
    package_dir = {
        '': '.',
    },
    install_requires = [ 'setuptools', ],
    cmdclass = cmdclass,
    data_files=data_files,
)

import psutil
import os
from PyQt5.QtCore import QSettings

def check_proc_exist(process_name):
    # print(os.path.join("/usr/share/applications", process_name+".desktop"))
    path = os.path.join("/usr/share/applications", process_name+".desktop")
    if os.path.exists(path):
        setting = QSettings(path,QSettings.IniFormat)
        setting.beginGroup("Desktop Entry")
        word_fullname = str(setting.value("Exec")).split(" ")[0]
        word = os.path.basename(word_fullname)
        pl = psutil.pids()
        for pid in pl:
            # print(psutil.Process(pid).name())
            # print(psutil.Process(pid).username())
            if word.startswith(psutil.Process(pid).name()) or word_fullname.startswith(psutil.Process(pid).name()):
                # print("exists:",psutil.Process(pid).name())
                return True
    return False

if __name__ == "__main__":
    check_proc_exist("kylin-video")
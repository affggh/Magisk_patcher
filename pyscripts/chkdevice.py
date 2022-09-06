import subprocess
import time

class chkdevice:
    def __init__(self):
        self.adb = "adb"
        # self.fastboot = "fastboot"
    def setadb(self, path):
        if type(path) != str:
            raise TypeError("adb path must be str")
        self.adb = path
    def setfastboot(self, path):
        if type(path) != str:
            raise TypeError("adb path must be str")
        self.fastboot = path

    def isAdbAlive(self):
        '''
        Windows only
        '''
        cmd = "tasklist"
        s = subprocess.check_output(cmd, encoding="gb2312", creationflags=subprocess.CREATE_NO_WINDOW)
        for i in s.splitlines():
            if i.startswith("adb.exe"):
                return True
        return False

    def chk_status(self, kill_adb=False):
        # if not isAdbAlive(): subprocess.getoutput("adb start-server") # 启动adb服务
        st_list = ['device', 'recovery', 'rescue', 'sideload', 'bootloader', 'disconnect']
        fb_list = ['fastboot']
        status = subprocess.getstatusoutput([self.adb, "get-state"])
        if status[0] == 0:
            for i in st_list:
                if status[1].strip(' ') == i:
                    return i
        else:
            status2 = subprocess.getoutput([self.fastboot, "devices"])
            if not status2.strip(' ')=='':
                return fb_list[0]
        return False
        if kill_adb:
            subprocess.getoutput([self.adb, "kill-server"])

    def loopUntil(self, state, maxretries=20, waitretries=1):
        for i in range(maxretries):
            if self.chk_status() == state:
                return True
            time.sleep(waitretries)
        if self.chk_status() == state:
            return True
        else:
            return False

    def getFastbootPartitionName(self):
        s = subprocess.getoutput([self.fastboot, "getvar", "all"])
        part = []
        for i in s.splitlines():
            if len(i.split(" "))>1:
                if i.split(" ")[1].split(":")[0].startswith("partition-type"):
                    part.append(i.split(" ")[1].split(":")[1])
        return part

import subprocess
import time, os

class chkdevice:
    def __init__(self):
        self.adb = "adb"
        self.fastboot = "fastboot"
    def setadb(self, path):
        if type(path) != str:
            raise TypeError("adb path must be str")
        self.adb = path
    def setfastboot(self, path):
        if type(path) != str:
            raise TypeError("adb path must be str")
        self.fastboot = path

    def runcmd(self, cmd):
        if os.name == 'posix':
            creationflags = 0
        elif os.name == 'nt':  # if on windows ,create a process with hidden console
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0
        ret = subprocess.run(cmd,
                                   shell=False,
                                   #stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   creationflags=creationflags
                                )
        return [ret.returncode, ret.stdout.decode('utf-8').strip('\n').strip('\r')]

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
        status = self.runcmd([self.adb, "get-state"])
        if status[0] == 0:
            for i in st_list:
                if status[1].strip(' ') == i:
                    return i
        else:
            status2 = self.runcmd([self.fastboot, "devices"])[1]
            if not status2.strip(' ')=='':
                return fb_list[0]
        if kill_adb:
            self.runcmd([self.adb, "kill-server"])
        return None

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
        s = self.runcmd([self.fastboot, "getvar", "all"])[1]
        part = []
        for i in s.splitlines():
            if len(i.split(" "))>1:
                if i.split(" ")[1].split(":")[0].startswith("partition-type"):
                    part.append(i.split(" ")[1].split(":")[1])
        return part

if __name__ == '__main__':
    c = chkdevice()
    print(c.chk_status())

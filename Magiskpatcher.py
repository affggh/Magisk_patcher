#!/usr/bin/env python3
import os, sys
import subprocess
import time
from tkinter import filedialog
import tkinter.font as tkfont
import webbrowser 
import requests
import tkinter as tk
import threading
import zipfile
import shutil

if os.name == 'nt':
    import ctypes
    # Tell system using self dpi adapt
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # get screen resize scale factor
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

# If not have module ttkbootstrap then auto download
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.scrolled import ScrolledText
except:
    if os.name == 'nt':
        os.system("pip install ttkbootstrap")
        os.system("pip install pillow")
    elif os.name == 'posix':
        if os.system("command -v pacman") == 0: # Arch linux
            os.system("sudo pacman -S python-pillow")
        if os.system("command -v apt") == 0: # Ubuntu
            os.system("sudo apt install python3-pil python3-pil.imagetk")
        else:
            sys.stderr.write("OS not support...\n")
            sys.exit(1)
        os.system("pip3 install ttkbootstrap")
        # os.system("pip3 install pillow")
    else:
        raise SystemError("Not support on %s" %os.name)
finally:
    import ttkbootstrap as ttk

try:  # For pyinstaller generate standlone program
    import pyscripts.splash as splash
except:
    pass

import pyscripts.mputils as mp  # some my own method
import pyscripts.archdetect as archdetect
from pyscripts.boot_patch import Patch
from pyscripts.chkdevice import chkdevice

VERSION = 20221101
AUTHOR = "affggh"

LOCALDIR = os.path.abspath(os.path.dirname(__file__))
RUNDIR = os.path.abspath(os.path.dirname(sys.argv[0]))

MAGISKGIT = "https://github.com/topjohnwu/Magisk"
MAGISKGITAPI = "https://api.github.com/repos/topjohnwu/Magisk/releases"
MAGISKPATCHERGIT = "https://github.com/affggh/Magisk_patcher"

os.chdir(RUNDIR)

class myStdout():	# 重定向类
    def __init__(self, text):
    	# 将其备份
        self.stdoutbak = sys.stdout		
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self
        self.text = text

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        self.text.insert('end', info)	# 在多行文本控件最后一行插入print信息
        self.text.update()	# 更新显示的文本，不加这句插入的信息无法显示
        self.text.see(tk.END)	# 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

class myApp(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.filename = ttk.StringVar()           # File name on file choose Entry
        self.Text = ttk.ScrolledText()        # Where log out
        self.progressBar = ttk.Progressbar()  # Progress bar
        self.progress = ttk.IntVar(value=0)    # Progress of progress bar

        self.arch = ttk.StringVar(value='arm64')
        self.keepverity = ttk.BooleanVar(value=True)
        self.keepforceencrypt = ttk.BooleanVar(value=True)
        self.patchvbmetaflag = ttk.BooleanVar(value=False)
        self.recoverymode = ttk.BooleanVar(value=False)
        self.verbose = ttk.BooleanVar(value=False)
        self.ostype, self.nativearch = archdetect.retTypeAndMachine()
        self.magisk = None
        self.gitmirror = ttk.StringVar(value=None)
        self.MAGISKLIST = []  # "magiskname"
        self.MAGISKDICT = {}  # "magiskname" : "download url"
        self.FillProgress = False
        # Make dir to download magisk apk
        if not os.path.isdir("prebuilt"):
            os.mkdir("prebuilt")
        self.__setupWidgets()

    def __fillProgress(self):
        while(self.FillProgress and self.progress.get()<79):
            self.progress.set(self.progress.get()+1)
            time.sleep(0.05)
    
    def fillProgress(self):
        self.FillProgress = True
        th = threading.Thread(target=self.__fillProgress)
        th.daemon = True
        th.start()
    
    def stopfillProgress(self):
        self.FillProgress = False

    def __chooseFile(self):
        f = filedialog.askopenfilename()
        if os.access(f, os.F_OK):
            self.filename.set(os.path.abspath(f))
        else:
            sys.stderr.write("Error: File does not exist...\n")

    def __tlog(self, t):
        self.Text.insert('end',
            "[%s]" %mp.retCurrentTime() + t
        )

    def __downloadFile(self, url, fileToSave):
        def p(now, total):
            return int((now/total)*100)
        file = fileToSave
        chunk_size = 1024
        try:
            r = requests.get(url, stream=True, allow_redirects=True)
        except:
            self.__tlog("网络异常或无法连接到目标链接...\n")
            return False
        self.__tlog("开始下载[%s] -> %s\n" %(url, fileToSave))
        total_size = int(r.headers['content-length'])
        now = 0
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    before = now
                    f.write(chunk)
                    now += chunk_size
                    if now > before:
                        self.progress.set(p(now, total_size))
        self.__tlog("下载完成\n")
        time.sleep(1)  # sleep 1 time to see 100%
        self.progress.set(0)
        return True

    def downloadFile(self, url, toSave):
        th = threading.Thread(target=self.__downloadFile, args=[url, toSave])
        th.daemon = True
        th.start()

    def __fixEnv(self):
        c = chkdevice()
        if os.name == 'nt':
            c.setadb(os.path.join(
                LOCALDIR, "bin", self.ostype, self.nativearch, "adb.exe"
            ))
        state = c.chk_status()
        print(state)
        if not state == "device" or state == "recovery":
            print("设备不存在")
            return

        if self.magisk != None:
            self.__parseApk()
        else:
            print("请先到修补页面选择一个magisk版本")
            return
        
        for i in ["magisk32", "magisk64", "magiskinit", "magiskboot", "busybox"]:
            if os.access(i, os.F_OK):
                shutil.move(i, os.path.join("assets", i))

        if os.name == 'nt':
            adb = os.path.join(LOCALDIR, "bin", self.ostype, self.nativearch, "adb")
        else:
            adb = "adb"

        su = ''
        print("- Detect root access")
        if mp.runcmd([adb, 'shell', 'whoami'])[1] != 'root':
            if mp.runcmd([adb, 'shell', 'su', '-v'])[0] != 0:
                print("! Cannot get su command and root access...")
                return
            else:
                print("- su command detect")
                su = 'su -c'

        print("- Remove old $MAGISKBIN")
        mp.runcmd([adb, "shell", su, "rm", "-rf", "/data/adb/magisk"])

        print("- Push new files")
        mp.runcmd([adb, "push", "assets", "/data/local/tmp/assets"])
        mp.runcmd([adb, "shell", su, "mv", "/data/local/tmp/assets", "/data/adb/magisk"])
        print("- Chmod&Chown files")
        mp.runcmd([adb, "shell", su, "chmod", "-R", "0755", "/data/adb/magisk/*"])
        mp.runcmd([adb, "shell", su, "chown", "-R", "0:0", "/data/adb/magisk"])
        print("- Done")

        self.cleanup()

    def __readFromDevice(self):
        def str2bool(var):
            if var.lower() == "true": return True
            else: return False
        def eq(var):
            return var.split("=")[0], var.split("=")[1]
        c = chkdevice()
        if os.name == 'nt':
            c.setadb(os.path.join(
                LOCALDIR, "bin", self.ostype, self.nativearch, "adb.exe"
            ))
        state = c.chk_status()
        print("读取的设备状态为[%s]" %state)
        if not state == "device" or state == "recovery":
            self.__tlog("设备未连接\n")
            return False
        if state == "device": tmp = "/data/local/tmp"
        else: tmp = "/tmp"
        configsh = os.path.join(LOCALDIR, "bin", "get_config.sh")
        cmds = [
            [c.adb, "push", configsh, tmp + "/" + "get_config.sh"],
            [c.adb, "shell", "chmod", "a+x", tmp + "/" + "get_config.sh"],
            [c.adb, "shell", "sh", tmp + "/" + "get_config.sh"]
        ]
        for cmd in cmds:
            retcode, ret = mp.runcmd(cmd)
            if retcode != 0:
                print("命令运行出错 :")
                print(cmd)
        print("读取出的配置为")
        for i in ret.splitlines():
            var, val = eq(i)
            print("\t%s[%s]" %(var.upper(),val.upper()))
            if var == "arch": self.arch.set(val)
            elif var == "keepverity": self.keepverity.set(str2bool(val))
            elif var == "keepforceencrypt": self.keepforceencrypt.set(str2bool(val))
            elif var == "patchvbmetaflag": self.patchvbmetaflag.set(str2bool(val))
        print("已自动修改第一页配置")
    
    def readFromDevice(self):
        th = threading.Thread(target=self.__readFromDevice)
        th.daemon = True
        th.run()

    def __parseApk(self):
        filename = RUNDIR + os.sep + "prebuilt" + os.sep + self.magisk + ".apk"
        def returnMagiskVersion(buf):
            v = "Unknow"
            l = buf.decode('utf_8').split("\n")
            for i in l:
                if not i.find("MAGISK_VER=") == -1:
                    v = i.split("=")[1].strip("'")
                    break
            return v
        def rename(n):
            if n.startswith("lib") and n.endswith(".so"):
                n = n.replace("lib", "").replace(".so", "")
            return n
        if not os.access(filename, os.F_OK):
            return False
        else:
            try:
                f = zipfile.ZipFile(filename, 'r')
            except:
                print("apk文件打开错误，不能识别为zip压缩包\n"
                      "请删除[%s]后更换镜像源重新下载" %filename)
                return
            l = f.namelist() # l equals list
            tl = []  # tl equals total get list
            for i in l:
                if i.startswith("assets/") or \
                   i.startswith("lib/"):
                    tl.append(i)

            buf = f.read("assets/util_functions.sh")
            mVersion = returnMagiskVersion(buf)
            print("Parse Magisk Version : " + mVersion + "\n")
            for i in tl:
                if i.startswith("assets"):
                    f.extract(i, "tmp")
                else:
                    if self.arch.get() == "arm64":
                        if i.startswith("lib/arm64-v8a/") and i.endswith(".so"):
                                f.extract(i, "tmp")
                    elif self.arch.get() == "arm":
                        if i.startswith("lib/armeabi-v7a/") and i.endswith(".so"):
                                f.extract(i, "tmp")
                    elif self.arch.get() == "x86_64":
                        if i.startswith("lib/x86_64/") and i.endswith(".so"):
                                f.extract(i, "tmp")
                    elif self.arch.get() == "x86":
                        if i.startswith("lib/x86/") and i.endswith(".so"):
                                f.extract(i, "tmp")
            for i in tl:
                if not i.startswith("assets"):
                    if self.arch.get() == "arm64" and not os.access("libmagisk32.so", os.F_OK):
                        if i == "lib/armeabi-v7a/libmagisk32.so":
                            f.extract("lib/armeabi-v7a/libmagisk32.so", "tmp")
                    elif self.arch.get() == "x86_64" and not os.access("libmagisk32.so", os.F_OK):
                        if i == "lib/x86/libmagisk32.so":
                            f.extract("lib/armeabi-v7a/libmagisk32.so", "tmp")
            f.close()
            shutil.move("tmp/assets/", "assets/")
            for root, dirs, files in os.walk("tmp"):
                for file in files:
                    if file.endswith(".so"):
                        shutil.move(root+os.sep+file, rename(os.path.basename(file)))
            if os.access("magiskpolicy", os.F_OK):
                shutil.move("magiskpolicy", "assets/magiskpolicy")
            shutil.rmtree("tmp")
            return True

    def __Patch(self):
        if not os.access(self.filename.get(), os.F_OK):
            self.__tlog("选中镜像文件不存在...\n")
            return False
        if self.magisk == None:
            self.__tlog("未选择magisk修补版本\n")
            return False
        if os.access(RUNDIR + os.sep + "new-boot.img", os.F_OK):  # Delete exist patched image before patch
            os.remove(RUNDIR + os.sep + "new-boot.img")
        if not self.__parseApk():
            self.__tlog("Error : Cannot parse apk file...\n")
            return False
        self.progress.set(20)
        self.fillProgress()
        p = Patch(self.keepverity.get(),
                  self.keepforceencrypt.get(),
                  self.patchvbmetaflag.get(),
                  self.recoverymode.get(),
                  self.verbose.get())
        p.setmagiskboot(LOCALDIR + os.sep +
                        "bin" + os.sep + 
                        self.ostype + os.sep +
                        self.nativearch + os.sep +
                        "magiskboot")
        p.patchboot(self.filename.get())
        self.stopfillProgress()
        self.progress.set(80)
        if os.access("new-boot.img", os.F_OK):
            self.progress.set(100)
            self.progressBar.stop()
            sys.stdout.write("- Done\n")
        else:
            self.progress.set(0)
            self.progressBar.stop()
            sys.stderr.write("- Failed\n")
        self.cleanup()
        self.progress.set(0)
    
    def cleanup(self):
        def delete(p):
            if os.path.isfile(p):
                os.remove(p)
            elif os.path.isdir(p):
                shutil.rmtree(p)
        rmlist = [
            "magisk32",
            "magisk64",
            "magiskinit",
            "magiskboot",
            "busybox",
            "header",
            "kernel",
            "ramdisk.cpio",
            "extra",
            "kernel_dtb",
            "recovery_dtbo",
            "dtb",
            "magiskpolicy",
            "assets"
        ]
        print("- Clean Up ...")
        for i in  rmlist: delete(i)

    def Patch(self):
        th = threading.Thread(target=self.__Patch)
        th.daemon = True
        th.start()
        
    def __setupWidgets(self):
        def setupFilechoose():
            fileFrame = ttk.Frame(self)
            fileLabel = ttk.Label(fileFrame, text="选择文件")
            fileEntry = ttk.Entry(fileFrame, textvariable=self.filename)
            fileButton = ttk.Button(fileFrame, text="选择文件", command=self.__chooseFile)
            
            fileFrame.pack(side='top', expand='no', fill='x', pady=5)
            fileLabel.pack(side='left', expand='no', padx=5)
            fileEntry.pack(side='left', expand='yes', fill='x', padx=5)
            fileButton.pack(side='left', expand='no', padx=5)
        
        def setupNotebook():
            def confirm():
                print("确认配置如下\n",
                      "\t架构 [%s]\n" %self.arch.get(),
                      "\t保持验证 [%s]\n" %self.keepverity.get(),
                      "\t保持强制加密 [%s]\n" %self.keepforceencrypt.get(),
                      "\t修补vbmeta标志 [%s]\n" %self.patchvbmetaflag.get(),
                      "\tRecovery修补 [%s]\n" %self.recoverymode.get())
                notebook.select(tab_patch)
            def getMagiskList(online=False):
                def getCurrent():
                    l = []
                    for root, dir, name in os.walk(RUNDIR + os.sep + "prebuilt"):
                        for i in name:
                            if i.endswith(".apk"):
                                l.append(i.strip(".apk"))
                    return l
                self.MAGISKLIST = []  # Reset magisk list

                if online:
                    self.__tlog("联网获取Magisk版本...\n")
                    self.MAGISKDICT = mp.getReleaseList(MAGISKGITAPI)
                    for i in self.MAGISKDICT.keys():
                        self.MAGISKLIST.append(i.strip(".apk"))
                for i in getCurrent():
                    if not i.strip(".apk") in self.MAGISKLIST:
                        self.MAGISKLIST.append(i.strip(".apk"))
                self.MAGISKLIST.sort(reverse=True)
                return self.MAGISKLIST
            def __updateTree(online=False):
                tree = magiskMenu.get_children()
                for i in tree:
                    magiskMenu.delete(i)
                self.progressBar.start()
                for i in getMagiskList(online):
                    magiskMenu.insert('', 'end', text=i, values=i)
                self.progressBar.stop()
            def updateTree(online=False):
                th = threading.Thread(target=lambda:__updateTree(online))
                th.daemon = True
                th.start()
            def selectMagisk(event):
                def exist(infile):
                    if os.access(infile, os.F_OK):
                        return True
                    else:
                        return False
                try:
                    self.magisk = magiskMenu.set(magiskMenu.focus())['magisk']
                except:
                    self.magisk = None
                if not exist(RUNDIR+os.sep+"prebuilt"+os.sep+self.magisk+".apk"):
                    self.__tlog("选中文件不存在，尝试从网络下载...\n")
                    if self.gitmirror.get() != "":
                        url = self.MAGISKDICT[self.magisk+".apk"].replace("https://github.com", self.gitmirror.get())
                    if self.gitmirror.get().find("cdn.jsdelivr.net") >= 0:
                        url = mp.magiskVresion2jsdelivr(self.magisk)
                    try:
                        self.downloadFile(url, "prebuilt"+os.sep+self.magisk+".apk")
                    except:
                        self.__tlog("下载失败...请手动将magisk apk格式安装包放入prebuilt文件夹内...\n")
            def verboseState(event):
                def boolReverse(b):
                    if b: return False 
                    else: return True
                self.__tlog("输出详细信息[%s]\n" %boolReverse(self.verbose.get()))
            def getAvailableGitMirror():
                l = []
                if os.access(LOCALDIR + os.sep + "gitmirrorlist.txt", os.F_OK):
                    with open(LOCALDIR + os.sep + "gitmirrorlist.txt", 'r') as f:
                        for i in f.readlines():
                            l.append(i.strip('\n'))
                    return l
                else:
                    return ["https://github.com", 
                            "https://download.fastgit.org",
                            "https://gh.api.99988866.xyz/https://github.com", 
                            "https://kgithub.com", 
                            "https://cdn.jsdelivr.net"]
            noteFrame = ttk.Frame(self)
            notebook = ttk.Notebook(noteFrame)
            tab_config = ttk.Frame(notebook)
            tab_patch = ttk.Frame(notebook)
            tab_else = ttk.Frame(notebook)

            # Text
            self.Text = ScrolledText(noteFrame, height=3, width=100, autohide=True, bootstyle="round")
            self.Text.pack(side='right', expand='no', fill='both',padx=5, pady=5)

            # Tab config
            arch_Frame = ttk.LabelFrame(tab_config, text="架构", labelanchor='nw')
            available_arch = ['arm64', 'arm', 'x86', 'x86_64']
            #archMenu = ttk.Combobox(arch_Frame, textvariable=self.arch, values=available_arch)
            for itm in available_arch:
                archMenu = ttk.Radiobutton(arch_Frame, text=itm, variable=self.arch, value=itm, bootstyle="toolbutton-success-outline")
                archMenu.pack(side='top', expand='no', fill='x',padx=5, pady=0, anchor='w')

            arch_Frame.pack(side='top', expand='yes', fill='x', ipady=5)

            check_keepverity = ttk.Checkbutton(tab_config, text="保持验证", bootstyle="square-toggle", variable=self.keepverity)
            check_keepforceenc = ttk.Checkbutton(tab_config, text="保持强制加密", bootstyle="square-toggle", variable=self.keepforceencrypt)
            check_vbpatchflag = ttk.Checkbutton(tab_config, text="修补vbmeta标志", bootstyle="square-toggle", variable=self.patchvbmetaflag)
            check_recovery = ttk.Checkbutton(tab_config, text="recovery修补", bootstyle="square-toggle", variable=self.recoverymode)

            check_keepverity.pack(side='top', anchor="w", padx=5, pady=5)
            check_keepforceenc.pack(side='top', anchor="w", padx=5, pady=5)
            check_vbpatchflag.pack(side='top', anchor="w", padx=5, pady=5)
            check_recovery.pack(side='top', anchor="w", padx=5, pady=5)

            # confirm button
            confirm_button = ttk.Button(tab_config, text='确认配置', command=confirm)
            confirm_button.pack(side='bottom', expand='no', padx=5, pady=5, fill='x')

            # patch Treeview
            magiskMenu = ttk.Treeview(tab_patch, show='', height=12, columns='magisk')
            magiskMenu.pack(side='top', expand='no', fill='both', padx=5, pady=5)
            magiskMenu.column('magisk', width=5, anchor='w')
            updateTree(False)
            magiskMenu.bind("<ButtonRelease-1>", selectMagisk)

            # get magisk versions
            getMagiskButton = ttk.Button(tab_patch, text="获取magisk版本", command=lambda online=True:updateTree(online))
            getMagiskButton.pack(side='top', expand='no', fill='x', padx=5, pady=5)

            #patch button
            patchButton = ttk.Button(tab_patch, text="修补boot镜像", command=self.Patch, bootstyle="success")
            patchButton.pack(side='top', expand='no', fill='x', padx=5, pady=5)

            # Debug checkbutton
            debugCheck = ttk.Checkbutton(tab_else, variable=self.verbose, text="Debug", bootstyle="square-warning-toggle")
            debugCheck.pack(side='top', expand='no', padx=5, pady=5, fill='x')
            debugCheck.bind("<ButtonRelease-1>", verboseState)

            # github mirror
            ttk.Separator(tab_else).pack(side='top', fill='x', padx=5, pady=5, expand='no')
            ttk.Label(tab_else, text="github镜像源", anchor='w').pack(side='top', padx=5, pady=5, fill='x')
            available_gitmirror = getAvailableGitMirror()
            gitMirrorCombobox = ttk.Combobox(tab_else, values=available_gitmirror, textvariable=self.gitmirror, width=15)
            gitMirrorCombobox.set(available_gitmirror[1])
            gitMirrorCombobox.pack(side='top', fill='x', expand='no', padx=5, pady=5)

            # Read config from device
            ttk.Separator(tab_else).pack(side='top', fill='x', padx=5, pady=5, expand='no')
            readButton = ttk.Button(tab_else, text="连接设备读取配置", command=self.readFromDevice)
            readButton.pack(side='top', padx=5, pady=5, fill='x', expand='no')

            # Fix magisk environment
            ttk.Separator(tab_else).pack(side='top', fill='x', padx=5, pady=5, expand='no')
            fixEnvButton = ttk.Button(tab_else, text="修复Magisk运行环境", command=self.__fixEnv, style="warning")
            fixEnvButton.pack(side='top', padx=5, pady=5, fill='x', expand='no')

            tab_config.pack(side='top')
            tab_patch.pack(side='top')
            tab_else.pack(side='top')
            notebook.add(tab_config, text="配置")
            notebook.add(tab_patch, text='修补')
            notebook.add(tab_else, text='其他')
            notebook.pack(side='left', expand='no', fill='y', padx=5, pady=5)
            noteFrame.pack(side='top', expand='yes', fill='both', padx=5, pady=5)

        def setupBottom():
            def cleanInfo():
                self.Text.delete(1.0, 'end')  # 清空text
            def donate():
                cleanInfo()
                self.Text.image_create('end', image=WECHAT)
                self.Text.image_create('end', image=ALIPAY)
                self.Text.image_create('end', image=ALIPAYHB)
            bottomFrame = ttk.Frame(self)
            cleanButton = ttk.Button(bottomFrame, text='清理信息', command=cleanInfo)
            donateButton = ttk.Button(bottomFrame, text='捐赠', command=donate, bootstyle="danger")
            cleanButton.pack(side='right', expand='no', padx=5, pady=5)
            donateButton.pack(side='right', expand='no', padx=5, pady=5)

            # progress Bar
            progressFrame = ttk.LabelFrame(bottomFrame, text='进度条', labelanchor='w')
            self.progressbar = ttk.Progressbar(progressFrame, variable=self.progress, mode='determinate', bootstyle="info")
            self.progressbar.pack(side='left', expand='yes', fill='x', padx=(15,0), anchor='e')
            precent = ttk.Label(progressFrame, textvariable=self.progress, width=3, anchor='e')
            precent.pack(side='left')
            ttk.Label(progressFrame, text="%").pack(side='left', padx=(0,5))
            progressFrame.pack(side='left', expand='yes', fill='x', padx=10, ipadx=5)

            bottomFrame.pack(side='top', expand='yes', fill='x')

        # Setup all widgets
        setupFilechoose()
        setupNotebook()
        setupBottom()

if __name__ == '__main__':
    def change_theme(theme):
        root.style.theme_use(theme)
        # log("切换主题[%s]" %(theme))

    def aboutUs():
        introduce = '''\
    Magisk Patcher by %s Version:%s
    这是一个可以在电脑上修补任意架构的简单小工具\
''' %(AUTHOR, VERSION)
        win = ttk.Toplevel(root)
        win.title("关于")
        # win.geometry("360x280")
        if os.name == 'nt':
            win.tk.call('tk', 'scaling', ScaleFactor/75)
        win.update()
        win.minsize(win.winfo_width(), win.winfo_height())
        x_cordinate = int((win.winfo_screenwidth() / 2) - (win.winfo_width() / 2))
        y_cordinate = int((win.winfo_screenheight() / 2) - (win.winfo_height() / 2))
        win.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        logofont = tkfont.Font(family="Gabriola", size=50, weight=tkfont.BOLD)
        logo = ttk.Label(win, text='Magisk Patcher', font=logofont, anchor="center")
        label = ttk.Label(win, image=LOGOIMG)
        button_about = ttk.Button(win, text="浏览项目地址", command=lambda:webbrowser.open(MAGISKPATCHERGIT))
        button_about.pack(side='bottom', anchor='e', expand='no', padx=10)
        label.pack(side='top', anchor='center', padx=5, pady=5)
        logo.pack(side='top', expand='no')
        ttk.Label(win, text=introduce, anchor='center').pack(side='top', expand='no')

    def setupMenubar():
        menubar = ttk.Menu(root)
        menubar_theme = ttk.Menu(menubar)
        for i in ttk.Style().theme_names():
            menubar_theme.add_command(label=i, command=lambda x=i:change_theme(x))
        menubar.add_cascade(label="主题", menu=menubar_theme)
        menubar.add_cascade(label="关于", command=lambda:aboutUs())
        root['menu'] = menubar

    root = ttk.Window(
        title="Magisk Patcher"
        # size=(WIDTH, HEIGHT),
    )

    # Fix high dpi issue
    if os.name == 'nt':
        root.tk.call('tk', 'scaling', ScaleFactor/75)

    # Setup images
    LOGOIMG = ttk.PhotoImage(file=LOCALDIR + os.sep + "bin" + os.sep + "logo.png")
    WECHAT = ttk.PhotoImage(file=LOCALDIR + os.sep + "bin" + os.sep + "wechat.png")
    ALIPAY = ttk.PhotoImage(file=LOCALDIR + os.sep + "bin" + os.sep + "alipay.png")
    ALIPAYHB = ttk.PhotoImage(file=LOCALDIR + os.sep + "bin" + os.sep + "zfbhb.png")

    setupMenubar()

    myapp = myApp(root)
    myapp.pack(side='top', expand='no', fill='both')

    myStd = myStdout(myapp.Text)

    OSTYPE , MACHINE = archdetect.retTypeAndMachine()
    introduce = '''\
\tMagisk Patcher %s by %s
\t\tYour native OS[%s] ARCH[%s]
Github 下载加速使用fastgit \n\t[https://doc.fastgit.org]
Magisk@topjohnwu\n\t[%s]
Magisk releases 获取使用Github的api \n\t[%s]
''' %(VERSION, AUTHOR, OSTYPE, MACHINE, MAGISKGIT, MAGISKGITAPI)

    myapp.Text.insert('end', introduce)

    root.resizable(0, 0)
    root.update()
    position = (( root.winfo_screenwidth() / 2 ) - ( root.winfo_width() / 2 ), \
                ( root.winfo_screenheight() / 2 ) - ( root.winfo_height() / 2 ))
    root.geometry("+%d+%d" %position)
    if os.name == 'nt':  # not work on linux
        root.iconbitmap(LOCALDIR +  os.sep + "bin" + os.sep + "logo.ico")

    root.mainloop()

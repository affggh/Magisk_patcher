#!/usr/bin/env python3
# 脚本 by affggh
# Apcache 2.0 
import os
import sys
import shutil
import zipfile
import subprocess
import platform
import requests
if os.name == 'nt':
    import tkinter as tk
if os.name == 'posix':
    from mttkinter import mtTkinter as tk 
    # While Load some need thread funcion on Linux it will failed
    # Just use mttkinter replace regular tkinter
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import *
#import ttkbootstrap as ttk
import time
import webbrowser
import threading

# Hide console , need ```pip install pywin32```
# import win32gui, win32con
# the_program_to_hide = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

def main():

    VERSION = "20220611"
    LOCALDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    # Read config from GUIcfg.txt
    configPath = LOCALDIR + os.sep + "bin" + os.sep + "GUIcfg.txt"
    with open(configPath, "r") as file:
        for line in file.readlines():
            if((line.split('=', 1)[0]) == "THEME"):
                THEME = line.split('=', 1)[1]
                THEME = THEME.replace('\n', '')
                if(THEME!="dark"): # 防止手贱改成别的导致主题爆炸
                    THEME="light"
            elif((line.split('=', 1)[0]) == "DONATE_BUTTON"):
                SHOW_DONATE_BUTTON = line.split('=', 1)[1]
                SHOW_DONATE_BUTTON = SHOW_DONATE_BUTTON.replace('\n', '') #显示捐赠按钮
            elif((line.split('=', 1)[0]) == "GIT_USE_MIRROR"):
                if (line.split('=', 1)[1].strip("\n").lower()) == "true":
                    GIT_USE_MIRROR = True
                else:
                    GIT_USE_MIRROR = False
            elif((line.split('=', 1)[0]) == "GIT_MIRROR"):
                GIT_MIRROR = line.split('=', 1)[1]

    # Detect machine and ostype
    ostype = platform.system().lower()
    machine = platform.machine().lower()
    if machine == 'aarch64_be' \
    or machine == 'armv8b' \
    or machine == 'armv8l':
        machine = 'aarch64'
    if machine == 'i386' or machine == 'i686':
        machine = 'x86'
    if machine == "amd64":
        machine = 'x86_64'
    if ostype == 'windows':
        if not machine == 'x86_64':
            print("Error : Program on windows only support 64bit machine")
            sys.exit(1)
    if ostype == 'linux':
        if not (machine == 'aarch64' or \
                machine == 'arm' or \
                machine == 'x86_64'):
            print("Error : Machine not support your device [%s]" %machine)
            sys.exit(1)
    

    root = tk.Tk()
    root.geometry("820x480")

    # Set the initial theme
    root.tk.call("source", LOCALDIR+os.sep+"sun-valley.tcl")
    root.tk.call("set_theme", THEME)

    def change_theme():
        # NOTE: The theme's real name is sun-valley-<mode>
        if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
            # Set light theme
            root.tk.call("set_theme", "light")
        else:
            # Set dark theme
            root.tk.call("set_theme", "dark")

    root.resizable(0,0) # 设置最大化窗口不可用
    root.title("Magisk Patcher by 酷安 affggh    " + "版本号 : %s" %(VERSION))

    def logo():
        os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
        root.iconbitmap(os.path.abspath(LOCALDIR+os.sep+'bin' + os.sep+ 'logo.ico'))
    if os.name == 'nt':
        logo()

    # Frame 这里都用到了外部命令导致卡顿，子进程运行来缓解
    frame2_3 = Frame(root, relief=FLAT)
    frame2 = ttk.LabelFrame(frame2_3, text="功能页面", labelanchor="n", relief=SUNKEN, borderwidth=1)
    frame3 = ttk.LabelFrame(frame2_3, text="信息反馈", labelanchor="nw", relief=SUNKEN, borderwidth=1)
    textfont = "Consolas"
    text = Text(frame3,width=70,height=15,font=textfont) # 信息展示

    filename = tk.StringVar()
    arch = tk.StringVar()
    keepverity = tk.StringVar()
    keepforceencrypt = tk.StringVar()
    patchvbmetaflag = tk.StringVar()
    mutiseletion = tk.StringVar()
    recoverymodeflag = tk.BooleanVar()
    recoverymode = tk.StringVar()

    recoverymode.set('false')
    # For logo
    photo = tk.PhotoImage(file=LOCALDIR+os.sep+"bin"+os.sep+"logo.png")#file：t图片路径
    # For aboutme
    photo2 = tk.PhotoImage(file=LOCALDIR+os.sep+"bin"+os.sep+"logo.png")#file：t图片路径
    # For donate QR code
    photo3 = tk.PhotoImage(file=LOCALDIR+os.sep+"bin"+os.sep+"alipay.png")#file：t图片路径
    photo4 = tk.PhotoImage(file=LOCALDIR+os.sep+"bin"+os.sep+"wechat.png")#file：t图片路径
    photo5 = tk.PhotoImage(file=LOCALDIR+os.sep+"bin"+os.sep+"zfbhb.png")#file：t图片路径

    global Thanks

    Thanks = 0 # 左下角的贴图说谢谢

    os.chdir(LOCALDIR)

    def get_time():

        '''显示当前时间'''

        global time1
        time1 = ''
        time2 = time.strftime('%H:%M:%S')
        # 能动态显示系统时间
        if time2 != time1:
            time1 = time2
            text.insert(END, "[%s] : " %(time1))

    def selectFile():
        global filepath
        filepath = askopenfilename()                   # 选择打开什么文件，返回文件名
        filename.set(os.path.abspath(filepath))
        showinfo("选择文件为：\n%s" %(filename.get()))

    def showinfo(textmsg):
        textstr = textmsg
        get_time() # 获取时间戳
        text.insert(END,"%s" %(textstr) + "\n")
        text.update() # 实时返回信息
        text.yview('end')

    def affgghsay(word):
        line = ''
        for i in range(len(word.encode("gb2312"))):
            line += '─'  # gb2312中文是两个字节，利用这点填充全角半角
        text.insert(END, 
'''
  (\︵/)   ┌%s┐
 >(—﹏—)< < %s│
  / ﹌ \╯  └%s┘
 affggh 提醒您
'''%(line, word, line))
        text.yview('end')

    def runcmd(cmd):
        if os.name == 'nt':
            sFlag = False
        else:
            sFlag = True  # fix file not found on linux
        try:
            ret = subprocess.Popen(cmd, shell=sFlag, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for i in iter(ret.stdout.readline, b''):
                text.insert(END, i.strip().decode("UTF-8") + "\n")
                text.update()
                text.yview(END)
        except subprocess.CalledProcessError as e:
            for i in iter(e.stdout.readline,b''):
                text.insert(END, i.strip().decode("UTF-8") + "\n")
                text.update()
                text.yview(END)

    def get_releases(url):
        data = requests.get(url).json()
        return data

    def ret_dlink(url):
        data = get_releases(url)
        dlink = {}
        for i in data:
            for j in i['assets']:
                if j['name'].startswith("Magisk-v") and j['name'].endswith(".apk"):
                    if GIT_USE_MIRROR:
                        dlink.update({j['name'] : j['browser_download_url'].replace("https://github.com/", GIT_MIRROR)})
                    else:
                        dlink.update({j['name'] : j['browser_download_url']})
        return dlink

    def download(url, fileToSave):
        def p(now, total):
            return int((now/total)*100)
        file = fileToSave
        chunk_size = 1024
        affgghsay("Starting download file...")
        r = requests.get(url, stream=True)
        total_size = int(r.headers['content-length'])
        now = 0
        progressbar['maximum'] = 100
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    before = now
                    f.write(chunk)
                    now += chunk_size
                    if now > before:
                        # print("下载进度 [%s/100]" %progress(now, total_size), end='\r')
                        progress.set(p(now, total_size))
        progress.set(0)
        affgghsay("文件下载完成"+file)

    def thrun(fun):  # 调用子线程跑功能，防止卡住
        # showinfo("Test threading...")
        th=threading.Thread(target=fun)
        th.daemon = True
        th.start()

    def cleaninfo():
        text.delete(1.0, END)  # 清空text
        text.image_create(END,image=photo)
        text.insert(END,"        Copyright(R) affggh  Apache2.0\n" \
                        "\n        此脚本为免费工具，如果你花钱买了你就是大傻逼\n")

    def test():
        affgghsay("Testing...")

    def showConfig():
        affgghsay("确认配置信息")
        text.insert(END , "\n" + \
                 "             镜像架构 = " + "%s\n" %(arch.get()) + \
                 "             保持验证 = " + "%s\n" %(keepverity.get()) + \
                 "             保持强制加密 = " + "%s\n" %(keepforceencrypt.get()) + \
                 "             修补vbmeta标志 = "+ "%s\n" %(patchvbmetaflag.get()) +\
                 "             Recovery Mode = " + "%s\n" %(recoverymode.get()))
        tabControl.select(tab2)

    def selectConfig():
        configpath = askopenfilename()                   # 选择打开什么文件，返回文件名
        showinfo("从配置文件中读取：\n%s" %(configpath))
        if os.path.isfile(configpath):
            with open(configpath, 'r') as f:
                PatchConfig = {}
                for i in f.readlines():
                    if not i[0:1] == '#':
                        l = i.strip('\n').split('=')
                        if not i.find('=') == -1:
                            PatchConfig[l[0]] = l[1]
            arch.set(PatchConfig['arch'])
            keepverity.set(PatchConfig['keepverity'])
            keepforceencrypt.set(PatchConfig['keepforceencrypt'])
            patchvbmetaflag.set(PatchConfig['patchvbmetaflag'])
            recoverymode.set(PatchConfig['recoverymode'])
            if recoverymode.get() == 'true':
                recoverymodeflag.set(True)
            else:
                recoverymodeflag.set(False)
            # showConfig()
        else:
            affgghsay("取消选择config文件")

    def confirmConfig():
        showConfig()

    def __select(*args):
        affgghsay("选择Magisk版本为 : %s" %(mutiseletion.get()))
        if not os.access("." + os.sep + "prebuilt" + os.sep + mutiseletion.get() + ".apk", os.F_OK):
            affgghsay("你选择的版本文件不存在，正在下载...")
            try:
                download(dlink[mutiseletion.get()+".apk"], "."+os.sep+"prebuilt"+os.sep+mutiseletion.get()+".apk")
            except:
                affgghsay("出现错误，请关掉代理重试")

    def select(*args):
        th = threading.Thread(target=__select, args=args)
        th.daemon = True
        th.start()

    def recModeStatus():
        if recoverymodeflag.get()== True:
            affgghsay("开启recovery模式修补")
            recoverymode.set("true")
        else:
            affgghsay("关闭recovery模式修补")
            recoverymode.set("false")

    def parseZip(filename):
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
            f = zipfile.ZipFile(filename, 'r')
            l = f.namelist() # l equals list
            tl = []  # tl equals total get list
            for i in l:
                if not i.find("assets/") == -1 or \
                   not i.find("lib/") == -1:
                    tl.append(i)
            buf = f.read("assets/util_functions.sh")
            mVersion = returnMagiskVersion(buf)
            showinfo("Parse Magisk Version : " + mVersion)
            for i in tl:
                if arch.get() == "arm64":
                    if i.startswith("lib/arm64-v8a/") and i.endswith(".so"):
                        if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                            f.extract(i, "tmp")
                elif arch.get() == "arm":
                    if i.startswith("lib/armeabi-v7a/") and i.endswith(".so"):
                        if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                            f.extract(i, "tmp")
                elif arch.get() == "x86_64":
                    if i.startswith("lib/x86_64/") and i.endswith(".so"):
                        if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                            f.extract(i, "tmp")
                elif arch.get() == "x86":
                    if i.startswith("lib/x86/") and i.endswith(".so"):
                        if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                            f.extract(i, "tmp")
            for i in tl:
                if arch.get() == "arm64" and not os.access("libmagisk32.so", os.F_OK):
                    if i == "lib/armeabi-v7a/libmagisk32.so":
                        f.extract("lib/armeabi-v7a/libmagisk32.so", "tmp")
                elif arch.get() == "x86_64" and not os.access("libmagisk32.so", os.F_OK):
                    if i == "lib/x86/libmagisk32.so":
                        f.extract("lib/armeabi-v7a/libmagisk32.so", "tmp")
            for root, dirs, files in os.walk("tmp"):
                for file in files:
                    if file.endswith(".so"):
                        shutil.move(root+os.sep+file, rename(os.path.basename(file)))
            shutil.rmtree("tmp")
            return True

    def PatchonWindows():
        affgghsay(" ---->> 修补开始")
        progressbar['maximum'] = 3
        start_time = time.time()
        if not os.access(filename.get(), os.F_OK):
            affgghsay("待修补文件不存在")
            affgghsay(" <<---- 修补失败")
            return False

        # cmd = [LOCALDIR+os.sep+'magisk_patcher.bat','patch','-i','%s' %(filename.get()),'-a','%s' %(arch.get()),'-kv','%s' %(keepverity.get()),'-ke','%s' %(keepforceencrypt.get()),'-pv','%s' %(patchvbmetaflag.get()),'-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())]
        f = "." + os.sep + "prebuilt" + os.sep + mutiseletion.get() + ".apk"
        if not parseZip(f):
            affgghsay("apk文件解析失败")
            affgghsay(" <<---- 修补失败")
            return False
        progress.set(1)
        if os.name == 'nt':
            cmd = "." + os.sep + "bin" + os.sep + ostype + os.sep + machine + os.sep + "busybox ash "
        elif os.name == 'posix':
            cmd = "." + os.sep + "bin" + os.sep + ostype + os.sep + machine + os.sep + "busybox ash "
        else:
            showinfo("not support")
            progress.set(0)
            return False
        if not os.access("./bin/boot_patch.sh", os.F_OK):
            affgghsay("Error : 关键脚本丢失")
            progress.set(0)
            return False
        cmd += "." + os.sep + "bin" + os.sep + "boot_patch.sh  \"%s\"" %(filename.get())
        cmd += " %s" %keepverity.get()
        cmd += " %s" %keepforceencrypt.get()
        cmd += " %s" %patchvbmetaflag.get()
        cmd += " %s" %recoverymode.get()
        try:
            progress.set(2)
            thrun(runcmd(cmd)) # 调用子线程运行减少卡顿
        except:
            progress.set(0)
            affgghsay("Error : 出现问题，修补失败")
        progress.set(3)
        cleanUp()
        end_time = time.time()
        use_time = end_time - start_time
        affgghsay("    总共用时 [%.2f] s" %use_time)
        affgghsay(" <<--- 修补结束")
        progress.set(0)

    def GenDefaultConfig():
        affgghsay(" ---->> 生成选中配置")
        if os.path.isfile('.' + os.sep + 'config.txt'):
            os.remove('.' + os.sep + 'config.txt')
        with open("." + os.sep + "config.txt", 'w') as f:
            f.write("# VAR    TYPE\n")
            f.write("arch=%s\n" %(arch.get()) + \
                    "keepverity=%s\n" %(keepverity.get()) + \
                    "keepforceencrypt=%s\n" %(keepforceencrypt.get()) + \
                    "patchvbmetaflag=%s\n" %(patchvbmetaflag.get()) + \
                    "recoverymode=%s\n" %(recoverymode.get()) + \
                    "magisk=%s\n" %("." + os.sep + "prebuilt" + os.sep + mutiseletion.get() + ".apk") )
                    # magisk=%s not use on python program, only worked on batch version
        if os.path.isfile('.' + os.sep + 'config.txt'):
            affgghsay("确认配置信息：")
            text.insert(END, "\n" + \
                         "             镜像架构 = " + "%s\n" %(arch.get()) + \
                         "             保持验证 = " + "%s\n" %(keepverity.get()) + \
                         "             保持强制加密 = " + "%s\n" %(keepforceencrypt.get()) + \
                         "             修补vbmeta标志 = "+ "%s\n" %(patchvbmetaflag.get()) +\
                         "             Recovery Mode = " + "%s\n" %(recoverymode.get()))
            affgghsay("成功生成配置")
        else:
            affgghsay("选中配置生成失败")
        affgghsay(" <<---- 生成选中配置")

    def GetDeviceConfig():
        affgghsay(" ---->> 读取设备配置")
        affgghsay("    根据设备不同，生成速度也不同...请稍等...")
        if os.name == 'nt':
            cmd = "." + os.sep + "bin" + os.sep + ostype + os.sep + machine + os.sep + "adb get-state"
        elif os.name == 'posix':
            cmd = "adb get-state"
        else:
            affgghsay("系统不支持")
            return False
        deviceState = subprocess.getstatusoutput(cmd)
        if deviceState[0] == 1:
            affgghsay("设备未连接，或驱动未安装")
            return False
        elif deviceState[0] == 0:
            if os.name == 'nt':
                cmd = "." + os.sep + "bin" + os.sep + ostype + os.sep + machine + os.sep + "adb "
            elif os.name == 'posix':
                cmd = "adb "
            if deviceState[1].strip(" ").strip("\n") == 'device':
                tmppath = "/data/local/tmp"
            elif deviceState[1].strip(" ").strip("\n") == 'recovery':
                tmppath = "/tmp"
            else:
                affgghsay("不支持的设备状态")
                return False
            subprocess.getoutput(cmd + "push " + "." + os.sep + "bin" + os.sep + "get_config.sh %s/get_config.sh" %tmppath)
            subprocess.getoutput(cmd + "shell chmod a+x %s/get_config.sh" %tmppath)
            out = subprocess.getoutput(cmd + "shell sh %s/get_config.sh" %tmppath)
            for i in out.splitlines():
                if len(i.split("=")) > 1:
                    var = i.split("=")[0].strip(" ").lower()
                    t = i.split("=")[1].strip(" ").lower()
                    if var == 'arch':
                        arch.set(t)
                    elif var == 'keepverity':
                        keepverity.set(t)
                    elif var == 'keepforceencrypt':
                        keepforceencrypt.set(t)
                    elif var == 'patchvbmetaflag':
                        patchvbmetaflag.set(t)
                    affgghsay("自动修改配置%s为%s" %(var, t))
        else:
            affgghsay("设备未知状态")
            return False
        affgghsay(" <<---- 读取设备配置")

    def opensource():
        webbrowser.open("https://github.com/affggh/Magisk_Patcher")

    def About():
        root2 = tk.Toplevel()
        curWidth = 300
        curHight = 180
        # 获取屏幕宽度和高度
        scn_w, scn_h = root.maxsize()
        # print(scn_w, scn_h)
        # 计算中心坐标
        cen_x = (scn_w - curWidth) / 2
        cen_y = (scn_h - curHight) / 2
        # print(cen_x, cen_y)

        # 设置窗口初始大小和位置
        size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
        root2.geometry(size_xy)
        #root2.geometry("300x180")
        root2.resizable(0,0) # 设置最大化窗口不可用
        root2.title("关于脚本和作者信息")
        aframe1 = Frame(root2, relief=FLAT, borderwidth=1)
        aframe2 = Frame(root2, relief=FLAT, borderwidth=1)
        aframe1.pack(side=BOTTOM, expand=YES, pady=3)
        aframe2.pack(side=BOTTOM, expand=YES, pady=3)
        ttk.Button(aframe1, text='访问项目', command=opensource).pack(side=LEFT, expand=YES, padx=5)
        ttk.Button(aframe1, text='获取最新', command=lambda u="https://hub.fastgit.xyz/affggh/Magisk_patcher/archive/refs/heads/main.zip":webbrowser.open(u)).pack(side=LEFT, expand=YES, padx=5)
        ttk.Label(aframe2, text='脚本编写自affggh\nshell脚本提取修改自Magisk-v24.1安装包\n项目开源地址：github.com/affggh/Magisk_Patcher\n').pack(side=BOTTOM, expand=NO, pady=3)
        
        imgLabe2 = ttk.Label(aframe2,image=photo2)#把图片整合到标签类中
        imgLabe2.pack(side=TOP, expand=YES, pady=3)
        root2.mainloop()

    def donateme():
        cleaninfo()
        text.image_create(END,image=photo3)
        text.image_create(END,image=photo4)
        text.image_create(END,image=photo5)
        global Thanks
        if Thanks==0:
            Label(frame4,text='    ----------------------------\n' \
                              '  < 谢谢老板！老板发大财！|\n' \
                              '   ----------------------------').pack(side=LEFT, expand=NO, pady=3)
            Thanks = 1

    def color(value):
      digit = list(map(str, range(10))) + list("ABCDEF")
      if isinstance(value, tuple):
        string = '#'
        for i in value:
          a1 = i // 16
          a2 = i % 16
          string += digit[a1] + digit[a2]
        return string
      elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)

    def colorfuldonate():
        button = tk.Button(frame41, text='给我捐钱', width=12, height=1, command=donateme, bg="red", fg="white", font=('黑体', '14'))
        button.grid(row=0, column=1, padx=3, pady=0)
        while(True):
            r = 255
            g = 0
            b = 0
            for c in range(255):
                r = r-1
                g = g+1
                button.configure(bg=color((r,g,b)))
                time.sleep(0.000001)
            for c in range(255):
                g = g-1
                b = b+1
                button.configure(bg=color((r,g,b)))
                time.sleep(0.000001)
            for c in range(255):
                b = b-1
                r = r+1
                button.configure(bg=color((r,g,b)))
                time.sleep(0.000001)

    def pointdonate():
        lab = tk.Label(frame41, text='<<点我', font=('黑体', '14'))
        lab.grid(row=0, column=2, padx=2, pady=0)
        while(True):
            lab.configure(bg='#FFFF00',fg='#000000')
            time.sleep(0.1)
            lab.configure(bg='#9400D3',fg='#FFFFFF')
            time.sleep(0.1)

    def pointdonate2():
        lab = tk.Label(frame41, text='点我>>', font=('黑体', '14'))
        lab.grid(row=0, column=0, padx=2, pady=0)
        while(True):
            lab.configure(bg='#FFFF00',fg='#000000')
            time.sleep(0.1)
            lab.configure(bg='#9400D3',fg='#FFFFFF')
            time.sleep(0.1)

    def pdp():
        th2=threading.Thread(target=pointdonate)
        th2.setDaemon(True) #守护线程
        th2.start()
        th=threading.Thread(target=colorfuldonate)
        th.setDaemon(True) #守护线程
        th.start()
        th3=threading.Thread(target=pointdonate2)
        th3.setDaemon(True) #守护线程
        th3.start()

    def listdir(path):
        L=[] 
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.apk':
                    tmp = os.path.basename(os.path.join(root, file)).strip(".apk")
                    L.append(tmp)
        return L

    def cleanUp():
        def rm(p):
            if os.access(p, os.F_OK):
                if os.path.isdir(p):
                    shutil.rmtree(p)
                elif os.path.isfile(p):
                    os.remove(p)
                else:
                    os.remove(p)

        l = ["busybox", "magisk32", "magisk64", "magiskinit", "magiskboot"]
        d = ["tmp"]
        for i in l:
            rm(i)
        for i in d:
            rm(i)
        cmd = "." + os.sep + "bin" + os.sep + ostype + os.sep + machine + os.sep + "magiskboot cleanup"
        thrun(runcmd(cmd))

    def get_comboxlist():
        url = "https://api.github.com/repos/topjohnwu/Magisk/releases"
        l = []
        try:
            global dlink
            dlink = ret_dlink(url)
            for i in dlink.keys():
                l.append(i.replace(".apk", ""))
        except:
            affgghsay(" 从网络读取失败, 仅加载本地目录")
        for i in os.listdir("." + os.sep + "prebuilt"):
            if i.endswith(".apk"):
                l.append(os.path.basename(i).replace(".apk", ""))
        l2=list(set(l))
        l2.sort(key=l.index)
        comboxlist["values"] = l2
        if len(l) > 0:
            comboxlist.current(0)
        select()

    # button and text
    # Frame 1  文件选择
    frame1 = LabelFrame(root, text="文件选择", labelanchor="w", relief=FLAT, borderwidth=1)
    frame1.pack(side=TOP, fill=BOTH, padx=6, pady=8, expand=NO)
    # tk.Label(frame1, text='选择文件').pack(side=LEFT)
    ttk.Entry(frame1, width=70,textvariable=filename).pack(side=LEFT, expand=YES, fill=X, padx=10)
    ttk.Button(frame1, text='选择文件', command=selectFile).pack(side=LEFT)
    # 

    # Frame 2 功能页面

    frame2.pack(side=LEFT, fill=BOTH, padx=2, pady=3, expand=NO)
    tabControl = ttk.Notebook(frame2)
    tab1 = ttk.Frame(tabControl)  #增加新选项卡
    tab11 = ttk.Frame(tab1)
    tab111 = ttk.LabelFrame(tab11, text="镜像架构", labelanchor="n", relief=SUNKEN, borderwidth=1)
    tab111.pack(side=TOP, expand=NO, fill=BOTH)
    arch.set("arm64")
    ttk.Radiobutton(tab111, text='arm',variable=arch, value='arm').grid(row=0, column=0, padx=0, pady=0)
    ttk.Radiobutton(tab111, text='arm64',variable=arch, value='arm64').grid(row=0, column=1, padx=0, pady=0)
    ttk.Radiobutton(tab111, text='x86',variable=arch, value='x86').grid(row=1, column=0, padx=0, pady=0)
    ttk.Radiobutton(tab111, text='x86_64',variable=arch, value='x86_64').grid(row=1, column=1, padx=0, pady=0)
    tab112 = ttk.LabelFrame(tab11, text="保持验证", labelanchor="n", relief=SUNKEN, borderwidth=1)
    tab112.pack(side=TOP, expand=YES, fill=BOTH)
    keepverity.set("true")
    ttk.Radiobutton(tab112, text='是',variable=keepverity, value='true').grid(row=0, column=0, padx=0, pady=0)
    ttk.Radiobutton(tab112, text='否',variable=keepverity, value='false').grid(row=0, column=1, padx=10, pady=0)
    tab113 = ttk.LabelFrame(tab11, text="保持强制加密", labelanchor="n", relief=SUNKEN, borderwidth=1)
    tab113.pack(side=TOP, expand=YES, fill=BOTH)
    keepforceencrypt.set("true")
    ttk.Radiobutton(tab113, text='是',variable=keepforceencrypt, value='true').grid(row=0, column=0, padx=0, pady=0)
    ttk.Radiobutton(tab113, text='否',variable=keepforceencrypt, value='false').grid(row=0, column=1, padx=10, pady=0)
    tab113 = ttk.LabelFrame(tab11, text="修补vbmeta标志", labelanchor="n", relief=SUNKEN, borderwidth=1)
    tab113.pack(side=TOP, expand=YES, fill=BOTH)
    patchvbmetaflag.set("false")
    ttk.Radiobutton(tab113, text='是',variable=patchvbmetaflag, value='true').grid(row=0, column=0, padx=0, pady=0)
    ttk.Radiobutton(tab113, text='否',variable=patchvbmetaflag, value='false').grid(row=0, column=1, padx=10, pady=0)
    tab12 = ttk.Frame(tab1)
    tab11.pack(side=TOP, expand=YES, fill=BOTH)
    ttk.Button(tab12, text='确认配置', command=confirmConfig).pack(side=TOP, expand=YES, pady=3)
    ttk.Button(tab12, text='指定config.txt', command=selectConfig).pack(side=TOP, expand=YES, pady=2)
    tabControl.add(tab1, text='配置')  #把新选项卡增加到Notebook

    tab2 = ttk.Frame(tabControl)  #增加新选项卡
    ttk.Button(tab2, text='使用当前配置\n修 补', command=PatchonWindows).pack(side=TOP, expand=NO, pady=3)
    # ttk.Button(tab2, text='连接设备环境\n修 补', command=PatchonDevice).pack(side=TOP, expand=NO, pady=3)
    ttk.Label(tab2, text='使用设备环境修补不需要\n配置各种参数\n配置来源与设备').pack(side=BOTTOM, expand=NO, pady=3)
    ttk.Label(tab2, text='选择Magisk版本').pack(side=TOP, expand=NO, pady=3)
    ttk.Checkbutton(tab2, variable=recoverymodeflag, text="recovery修补", command=recModeStatus).pack(side=TOP, expand=NO, pady=3)
    comboxlist = ttk.Combobox(tab2, textvariable=mutiseletion, width=14)
    '''
    filelist = listdir("./prebuilt")
    filelist.reverse()  # 高版本在前面
    comboxlist["values"]=(filelist)
    if len(filelist)>0:
        comboxlist.current(0) # 选择第一个
    else:
        showinfo("Error : 没有找到Magisk安装包，请确保prebuilt目录下存在apk文件")
    '''
    # thrun(get_comboxlist())
    comboxlist.bind("<<ComboboxSelected>>",select)
    comboxlist.pack(side=TOP, expand=NO, pady=3)
    tabControl.add(tab2, text='修补')  #把新选项卡增加到Notebook
    ttk.Button(tab2, text='获取magisk列表', command=get_comboxlist).pack(side=TOP, expand=NO, pady=3)

    tab3 = tk.Frame(tabControl)  #增加新选项卡
    ttk.Button(tab3, text='生成选中配置\nconfig.txt', command=lambda:thrun(GenDefaultConfig)).pack(side=TOP, expand=NO, pady=3)
    ttk.Button(tab3, text='读取设备配置\nconfig.txt', command=lambda:thrun(GetDeviceConfig)).pack(side=TOP, expand=NO, pady=3)
    # ttk.Button(tab3, text='test', command=lambda:thrun(test)).pack(side=TOP, expand=NO, pady=3)
    tabControl.add(tab3, text='读取')  #把新选项卡增加到Notebook
    tab12.pack(side=TOP, expand=NO, fill=BOTH)
    tabControl.pack(side=TOP, expand=YES, fill="both")


    # Frame 3  信息展示 功能页面

    frame3.pack(side=RIGHT, fill=BOTH, padx=2, pady=3, expand=YES)

    scroll = ttk.Scrollbar(frame3)
    scroll.pack(side=RIGHT,fill=Y, padx=1, pady=5)
    text.pack(side=RIGHT, expand=YES, fill=BOTH, padx=5 ,pady=1)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    frame2_3.pack(side=TOP, expand=NO, pady=2, fill=BOTH)


    # Frame 4 关于 和 清除信息t
    frame4 = Frame(root, relief=FLAT)
    progress = tk.DoubleVar(value=0)
    progressbar = ttk.Progressbar(frame4, length=200, variable=progress, mode='determinate')
    ttk.Button(frame4, text='清空信息', command=cleaninfo).pack(side=RIGHT, expand=NO, pady=3)
    ttk.Button(frame4, text='关于', command=About).pack(side=RIGHT, expand=NO, pady=3)
    ttk.Button(frame4, text='切换主题', command=change_theme).pack(side=RIGHT, expand=NO, pady=3)
    if(SHOW_DONATE_BUTTON!="False"):
        # 超炫的捐赠按钮
        frame41 = Frame(frame4, relief=FLAT)
        pdp()
        frame41.pack(side=RIGHT, expand=NO, pady=3)
    else:
        ttk.Button(frame4, text='捐赠', command=donateme).pack(side=RIGHT, expand=NO, pady=3)
    progressbar.pack(side=RIGHT, expand=NO, padx=(0, 10))
    ttk.Label(frame4, text="进度条：").pack(side=RIGHT, expand=NO, padx=(10, 0))
    frame4.pack(side=TOP, expand=NO, padx=10, ipady=5, fill=X)

    imgLabel = ttk.Label(frame4,image=photo)#把图片整合到标签类中
    imgLabel.pack(side=LEFT, expand=NO, pady=3)

    text.image_create(END,image=photo)
    text.insert(END,"        Copyright(R) affggh  Apache2.0\n" \
                    "    当前脚本运行环境：\n" \
                    "                   [%s] [%s]\n" \
                    "此脚本为免费工具，如果你花钱买了你就是大傻逼\n" \
                    "普通流程：\n" \
                    "修改配置-->确认配置-->修补\n" \
                    "简单点：\n" \
                    "直接选个magisk版本-->插手机-->手机修补\n            （不过配置只能用手机的）\n" \
                    "  注：recovery模式仅支持windows修补\n" %(ostype, machine))
    affgghsay("此脚本为免费工具，如果你花钱买了你就是大傻逼")

    # root.update()
    root.mainloop()

if __name__=='__main__':
    main()

# 脚本 by affggh
# Apcache 2.0 
import os
import sys
import subprocess
import tkinter as tk 
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import *
#import ttkbootstrap as ttk
import time
import webbrowser
import threading

# Hide console , need ```pip install pywin32```
#import win32gui, win32con
#the_program_to_hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

VERSION = "20220304"
# Read config from GUIcfg.txt
configPath = ".\\bin\\GUIcfg.txt"
with open(configPath, "r") as file:
    for line in file.readlines():
        if((line.split('=', 1)[0]) == "THEME"):
            THEME = line.split('=', 1)[1]
            THEME = THEME.replace('\n', '')
            if(THEME!="dark"): # 防止手贱改成别的导致主题爆炸
                THEME="light"
        if((line.split('=', 1)[0]) == "DONATE_BUTTON"):
            SHOW_DONATE_BUTTON = line.split('=', 1)[1]
            SHOW_DONATE_BUTTON = SHOW_DONATE_BUTTON.replace('\n', '') #显示捐赠按钮

#print(THEME)
#print(SHOW_DONATE_BUTTON)

root = tk.Tk()
root.geometry("750x470")

# Set the initial theme
root.tk.call("source", "sun-valley.tcl")
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
    root.iconbitmap('bin\\logo.ico')

logo()

# Frame 这里都用到了外部命令导致卡顿，子进程运行来缓解
frame2_3 = Frame(root, relief=FLAT)
frame2 = ttk.LabelFrame(frame2_3, text="功能页面", labelanchor="n", relief=SUNKEN, borderwidth=1)
frame3 = ttk.LabelFrame(frame2_3, text="信息反馈", labelanchor="nw", relief=SUNKEN, borderwidth=1)
text = Text(frame3,width=70,height=15) # 信息展示

filename = tk.StringVar()
configname = tk.StringVar()
arch = tk.StringVar()
keepverity = tk.StringVar()
keepforceencrypt = tk.StringVar()
patchvbmetaflag = tk.StringVar()
mutiseletion = tk.StringVar()
recoverymode = tk.StringVar()
# For logo
photo = tk.PhotoImage(file=".\\bin\\logo.png")#file：t图片路径
# For aboutme
photo2 = tk.PhotoImage(file=".\\bin\\logo.png")#file：t图片路径
# For donate QR code
photo3 = tk.PhotoImage(file=".\\bin\\alipay.png")#file：t图片路径
photo4 = tk.PhotoImage(file=".\\bin\\wechat.png")#file：t图片路径
photo5 = tk.PhotoImage(file=".\\bin\\zfbhb.png")#file：t图片路径

global Configflag
Configflag = 0    # 默认使用第一页的配置

Thanks = 0 # 左下角的贴图说谢谢

def chdir():
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

chdir()

def get_time():

    '''显示当前时间'''

    global time1
    time1 = ''
    time2 = time.strftime('%H:%M:%S')
    # Label(top, text='当前时间:', bg='gold', font=28).place(x=630, y=120)
    # 能动态显示系统时间
    if time2 != time1:
        time1 = time2
        text.insert(END, "[%s] : " %(time1))
        # clock.configure(text=time2)
        # clock.place(x=715, y=120)
        # clock.after(200,get_time)

def selectFile():
    filepath = askopenfilename()                   # 选择打开什么文件，返回文件名
    filename.set(filepath.replace('/', '\\'))      # 设置变量filename的值
    showinfo("选择文件为：\n%s" %(filepath.replace('/', '\\')))

def showinfo(textmsg):
    textstr = textmsg
    get_time() # 获取时间戳
    text.insert(END,"%s" %(textstr) + "\n")
    text.update() # 实时返回信息
    text.yview('end')

def runcmd(cmd):
    try:
        ret = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for i in iter(ret.stdout.readline, b''):
            showinfo(i.strip().decode("UTF-8"))
    except subprocess.CalledProcessError as e:
        for i in iter(e.stdout.readline,b''):
            showinfo(i.strip().decode("UTF-8"))

def thrun(fun):  # 调用子线程跑功能，防止卡住
    # showinfo("Test threading...")
    th=threading.Thread(target=fun)
    th.setDaemon(True)
    th.start()

def cleaninfo():
    text.delete(1.0, END)  # 清空text
    text.image_create(END,image=photo)
    text.insert(END,"        Copyright(R) affggh  Apache2.0\n")
    text.insert(END,"\n        此脚本为免费工具，如果你花钱买了你就是大傻逼\n")

def test():
    showinfo("Testing...")

def showConfig(flag):
    global Configflag
    if(flag==1):
        Configflag = 1
        showinfo("脚本从config文件读取...")
        if(os.access(configname.get(), os.F_OK)):
            f = open(configname.get())
            line = f.readline()
            while line:
                showinfo(line.replace('\n', ''))
                line = f.readline()
            f.close()
    else:
        Configflag = 0
        showinfo("确认配置信息：")
        showinfo("             镜像架构 = " + "%s" %(arch.get()))
        showinfo("             保持验证 = " + "%s" %(keepverity.get()))
        showinfo("             保持强制加密 = " + "%s" %(keepforceencrypt.get()))
        showinfo("             修补vbmeta标志 = "+ "%s" %(patchvbmetaflag.get()))
    tabControl.select(tab2)

def selectConfig():
    configpath = askopenfilename()                   # 选择打开什么文件，返回文件名
    configname.set(configpath.replace('/', '\\'))      # 设置变量filename的值
    showinfo("选择配置文件为：\n%s" %(configpath.replace('/', '\\')))
    showConfig(1)

def confirmConfig():
    showConfig(0)

def select(*args):
    showinfo("选择Magisk版本为 : %s" %(mutiseletion.get()))

def recModeStatus():
    if recoverymode.get()=='1':
        showinfo("开启recovery模式修补")
    else:
        showinfo("关闭recovery模式修补")

def PatchonWindows():
    showinfo(" ---->> 修补开始")
    if(Configflag==1):
        cmd = ['.\\magisk_patcher.bat','patch','-i','%s' %(filename.get()),'-c','%s' %(configname.get())]
    else:
        cmd = ['.\\magisk_patcher.bat','patch','-i','%s' %(filename.get()),'-a','%s' %(arch.get()),'-kv','%s' %(keepverity.get()),'-ke','%s' %(keepforceencrypt.get()),'-pv','%s' %(patchvbmetaflag.get()),'-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())]
    if recoverymode.get()=='1':
        showinfo("启用recovery模式修补")
        cmd.append('-r')
        showinfo(cmd)
    thrun(runcmd(cmd)) # 调用子线程运行减少卡顿
    showinfo(" <<--- 修补结束")

def PatchonDevice():
    showinfo(" ---->> 使用设备环境修补开始")
    showinfo("    本功能信息回馈较慢，请耐心等待...")
    cmd = ['.\\magisk_patcher.bat','patchondevice','-i','%s' %(filename.get()),'-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())]
    thrun(runcmd(cmd))
    showinfo(" <<---- 使用设备环境修补结束")

def GenDefaultConfig():
    showinfo(" ---->> 生成默认配置")
    cmd = ['.\\magisk_patcher.bat','autoconfig','--default','-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())]
    thrun(runcmd(cmd))
    showinfo(" <<---- 生成默认配置")

def GetDeviceConfig():
    showinfo(" ---->> 读取设备配置")
    showinfo("    根据设备不同，生成速度也不同...请稍等...")
    cmd = ['.\\magisk_patcher.bat','autoconfig','-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())]
    thrun(runcmd(cmd))
    showinfo(" <<---- 读取设备配置")

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
    chdir()
    
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
        Label(frame4,text='    ----------------------------\n  < 谢谢老板！老板发大财！|\n   ----------------------------').pack(side=LEFT, expand=NO, pady=3)
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
    th2.setDaemon(True)#守护线程
    th2.start()
    th=threading.Thread(target=colorfuldonate)
    th.setDaemon(True)#守护线程
    th.start()
    th3=threading.Thread(target=pointdonate2)
    th3.setDaemon(True)#守护线程
    th3.start()

def listdir(path):
    L=[] 
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.apk':
                tmp = os.path.join(root, file)
                tmp = tmp.replace('.apk','')
                tmp = tmp.replace('.\\prebuilt\\','')
                L.append(tmp)
    return L

# button and text
# Frame 1  文件选择
frame1 = LabelFrame(root, text="文件选择", labelanchor="w", relief=FLAT, borderwidth=1)
frame1.pack(side=TOP, fill=BOTH, padx=6, pady=8, expand=NO)
# tk.Label(frame1, text='选择文件').pack(side=LEFT)
ttk.Entry(frame1, width=80,textvariable=filename).pack(side=LEFT, padx=10)
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
ttk.Button(tab2, text='Windows环境\n修 补', command=PatchonWindows).pack(side=TOP, expand=NO, pady=3)
ttk.Button(tab2, text='连接设备环境\n修 补', command=PatchonDevice).pack(side=TOP, expand=NO, pady=3)
ttk.Label(tab2, text='使用设备环境修补不需要\n配置各种参数\n配置来源与设备').pack(side=BOTTOM, expand=NO, pady=3)
ttk.Label(tab2, text='选择Magisk版本').pack(side=TOP, expand=NO, pady=3)
ttk.Checkbutton(tab2, variable=recoverymode, text="recovery修补", command=recModeStatus).pack(side=TOP, expand=NO, pady=3)
comboxlist = ttk.Combobox(tab2, textvariable=mutiseletion, width=14)
filelist = listdir(".\\prebuilt")
comboxlist["values"]=(filelist)
if(filename):
    comboxlist.current(0) # 选择第一个
else:
    showinfo("Error : 没有找到Magisk安装包，请确保prebuilt目录下存在apk文件")
comboxlist.bind("<<ComboboxSelected>>",select)
comboxlist.pack(side=TOP, expand=NO, pady=3)
tabControl.add(tab2, text='修补')  #把新选项卡增加到Notebook

tab3 = tk.Frame(tabControl)  #增加新选项卡
ttk.Button(tab3, text='生成默认配置\nconfig.txt', command=lambda:thrun(GenDefaultConfig)).pack(side=TOP, expand=NO, pady=3)
ttk.Button(tab3, text='读取设备配置\nconfig.txt', command=lambda:thrun(GetDeviceConfig)).pack(side=TOP, expand=NO, pady=3)
# tk.Button(tab3, text='test', width=12, height=3, command=lambda:thrun(PatchonWindows)).pack(side=TOP, expand=NO, pady=3)
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


# Frame 4 关于 和 清除信息
frame4 = Frame(root, relief=FLAT)
ttk.Button(frame4, text='清空信息', command=cleaninfo).pack(side=RIGHT, expand=NO, pady=3)
ttk.Button(frame4, text='关于', command=About).pack(side=RIGHT, expand=NO, pady=3)
ttk.Button(frame4, text='切换主题', command=change_theme).pack(side=RIGHT, expand=NO, pady=3)
if(SHOW_DONATE_BUTTON!="False"):
    # 超炫的捐赠按钮
    frame41 = Frame(frame4, relief=FLAT)
    pdp()
    frame41.pack(side=RIGHT, expand=NO, pady=3)
frame4.pack(side=TOP, expand=NO, padx=10, ipady=5, fill=BOTH)

imgLabel = ttk.Label(frame4,image=photo)#把图片整合到标签类中
imgLabel.pack(side=LEFT, expand=NO, pady=3)

text.image_create(END,image=photo)
text.insert(END,"        Copyright(R) affggh  Apache2.0\n")
showinfo("欢迎使用我的Magisk修补脚本")
showinfo("    脚本运行环境：")
showinfo("                 windows10 x86_64")
showinfo("此脚本为免费工具，如果你花钱买了你就是大傻逼")
showinfo("普通流程：")
showinfo("修改配置-->确认配置-->修补")
showinfo("高级点：")
showinfo("自己写个config.txt-->选择config.txt-->修补")
showinfo("简单点：")
showinfo("直接选个magisk版本-->插手机-->手机修补\n            （不过配置只能用手机的）")
showinfo("  注：recovery模式仅支持windows修补")
text.insert(END,"\n        此脚本为免费工具，如果你花钱买了你就是大傻逼\n")

root.update()
root.mainloop()
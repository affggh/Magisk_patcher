# 脚本 by affggh
import os
import sys
import subprocess
import tkinter as tk 
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import *
import time
import webbrowser

VERSION = "20220213"

root = tk.Tk()
root.geometry("640x440")

root.resizable(0,0) # 设置最大化窗口不可用
root.title("Magisk Patcher by 酷安 affggh    " + "版本号 : %s" %(VERSION))

def logo():
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    root.iconbitmap('bin\\logo.ico')

logo()

filename = tk.StringVar()
configname = tk.StringVar()
arch = tk.StringVar()
keepverity = tk.StringVar()
keepforceencrypt = tk.StringVar()
patchvbmetaflag = tk.StringVar()
mutiseletion = tk.StringVar()
# For logo
photo = tk.PhotoImage(file=".\\bin\\logo.png")#file：t图片路径
# For aboutme
photo2 = tk.PhotoImage(file=".\\bin\\logo.png")#file：t图片路径
# For donate QR code
photo3 = tk.PhotoImage(file=".\\bin\\alipay.png")#file：t图片路径
photo4 = tk.PhotoImage(file=".\\bin\\wechat.png")#file：t图片路径

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

def PatchonWindows():
    showinfo(" ---->> 修补开始")
    if(Configflag==1):
        try:
            cmd = subprocess.check_output(['.\\magisk_patcher.bat','patch','-i','%s' %(filename.get()),'-c','%s' %(configname.get())], shell=False,stderr=subprocess.STDOUT)
            showinfo('\n' + cmd.decode(encoding="utf-8"))
        except subprocess.CalledProcessError as e:
            showinfo('\n' + e.output.decode(encoding="utf-8"))
    else:
        try:
            cmd = subprocess.check_output(['.\\magisk_patcher.bat','patch','-i','%s' %(filename.get()),'-a','%s' %(arch.get()),'-kv','%s' %(keepverity.get()),'-ke','%s' %(keepforceencrypt.get()),'-pv','%s' %(patchvbmetaflag.get()),'-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())], shell=False,stderr=subprocess.STDOUT)
            showinfo('\n' + cmd.decode(encoding="utf-8"))
        except subprocess.CalledProcessError as e:
            showinfo('\n' + e.output.decode(encoding="utf-8"))
    showinfo(" <<--- 修补结束")

def PatchonDevice():
    showinfo(" ---->> 使用设备环境修补开始")
    showinfo("    本功能信息回馈较慢，请耐心等待...")
    try:
        cmd = subprocess.check_output(['.\\magisk_patcher.bat','patchondevice','-i','%s' %(filename.get()),'-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())], shell=False,stderr=subprocess.STDOUT)
        showinfo('\n' + cmd.decode(encoding="utf-8"))
    except subprocess.CalledProcessError as e:
        showinfo('\n' + e.output.decode(encoding="utf-8"))
    showinfo(" <<---- 使用设备环境修补结束")

def GenDefaultConfig():
    showinfo(" ---->> 生成默认配置")
    try:
        cmd = subprocess.check_output(['.\\magisk_patcher.bat','autoconfig','--default','-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())], shell=False,stderr=subprocess.STDOUT)
        showinfo('\n' + cmd.decode(encoding="utf-8"))
    except subprocess.CalledProcessError as e:
        showinfo('\n' + e.output.decode(encoding="utf-8"))
    showinfo(" <<---- 生成默认配置")

def GetDeviceConfig():
    showinfo(" ---->> 读取设备配置")
    showinfo("    根据设备不同，生成速度也不同...请稍等...")
    try:
        cmd = subprocess.check_output(['.\\magisk_patcher.bat','autoconfig','-m','.\\prebuilt\\%s.apk' %(mutiseletion.get())], shell=False,stderr=subprocess.STDOUT)
        showinfo('\n' + cmd.decode(encoding="utf-8"))
    except subprocess.CalledProcessError as e:
        showinfo('\n' + e.output.decode(encoding="utf-8"))
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
    tk.Button(aframe1, text='访问项目', width=12, height=1, command=opensource).pack(side=LEFT, expand=YES, padx=5)
    tk.Label(aframe2, text='脚本编写自affggh\nshell脚本提取修改自Magisk-v24.1安装包\n项目开源地址：github.com/affggh/Magisk_Patcher\n').pack(side=BOTTOM, expand=NO, pady=3)
    chdir()
    
    imgLabe2 = tk.Label(aframe2,image=photo2)#把图片整合到标签类中
    imgLabe2.pack(side=TOP, expand=YES, pady=3)
    root2.mainloop()

def donateme():
    cleaninfo()
    text.image_create(END,image=photo3)
    text.image_create(END,image=photo4)
    global Thanks
    if Thanks==0:
        Label(frame4,text='    ----------------------------\n  < 谢谢老板！老板发大财！|\n   ----------------------------').pack(side=LEFT, expand=NO, pady=3)
        Thanks = 1

# button and text
# Frame 1  文件选择
frame1 = LabelFrame(root, text="文件选择", labelanchor="w", relief=FLAT, borderwidth=1)
frame1.pack(side=TOP, fill=BOTH, padx=6, pady=3, expand=NO)
# tk.Label(frame1, text='选择文件').pack(side=LEFT)
tk.Entry(frame1, width=70,textvariable=filename).pack(side=LEFT, padx=10)
tk.Button(frame1, text='选择文件', command=selectFile).pack(side=LEFT)
# 
frame2_3 = Frame(root, relief=FLAT)
# Frame 2 功能页面
frame2 = LabelFrame(frame2_3, text="功能页面", labelanchor="n", relief=SUNKEN, borderwidth=1)
frame2.pack(side=LEFT, fill=BOTH, padx=2, pady=3, expand=YES)
tabControl = ttk.Notebook(frame2)
tab1 = tk.Frame(tabControl,bg='blue')  #增加新选项卡
tab11 = tk.Frame(tab1,bg='red')
tab111 = tk.LabelFrame(tab11, text="镜像架构", labelanchor="n", relief=SUNKEN, borderwidth=1)
tab111.pack(side=TOP, expand=NO, fill=BOTH)
arch.set("arm64")
tk.Radiobutton(tab111, text='arm',variable=arch, value='arm').grid(row=0, column=0, padx=0, pady=0)
tk.Radiobutton(tab111, text='arm64',variable=arch, value='arm64').grid(row=0, column=1, padx=0, pady=0)
tk.Radiobutton(tab111, text='x86',variable=arch, value='x86').grid(row=1, column=0, padx=0, pady=0)
tk.Radiobutton(tab111, text='x86_64',variable=arch, value='x86_64').grid(row=1, column=1, padx=0, pady=0)
tab112 = tk.LabelFrame(tab11, text="保持验证", labelanchor="n", relief=SUNKEN, borderwidth=1)
tab112.pack(side=TOP, expand=YES, fill=BOTH)
keepverity.set("true")
tk.Radiobutton(tab112, text='是',variable=keepverity, value='true').grid(row=0, column=0, padx=0, pady=0)
tk.Radiobutton(tab112, text='否',variable=keepverity, value='false').grid(row=0, column=1, padx=10, pady=0)
tab113 = tk.LabelFrame(tab11, text="保持强制加密", labelanchor="n", relief=SUNKEN, borderwidth=1)
tab113.pack(side=TOP, expand=YES, fill=BOTH)
keepforceencrypt.set("true")
tk.Radiobutton(tab113, text='是',variable=keepforceencrypt, value='true').grid(row=0, column=0, padx=0, pady=0)
tk.Radiobutton(tab113, text='否',variable=keepforceencrypt, value='false').grid(row=0, column=1, padx=10, pady=0)
tab113 = tk.LabelFrame(tab11, text="修补vbmeta标志", labelanchor="n", relief=SUNKEN, borderwidth=1)
tab113.pack(side=TOP, expand=YES, fill=BOTH)
patchvbmetaflag.set("false")
tk.Radiobutton(tab113, text='是',variable=patchvbmetaflag, value='true').grid(row=0, column=0, padx=0, pady=0)
tk.Radiobutton(tab113, text='否',variable=patchvbmetaflag, value='false').grid(row=0, column=1, padx=10, pady=0)
tab12 = tk.Frame(tab1)
tab11.pack(side=TOP, expand=YES, fill=BOTH)
tk.Button(tab12, text='确认配置', width=12, height=1, command=confirmConfig).pack(side=TOP, expand=YES, pady=3)
tk.Button(tab12, text='指定config.txt', width=12, height=1, command=selectConfig).pack(side=TOP, expand=YES, pady=2)
tabControl.add(tab1, text='配置')  #把新选项卡增加到Notebook

tab2 = tk.Frame(tabControl)  #增加新选项卡
tk.Button(tab2, text='Windows环境\n修 补', width=12, height=3, command=PatchonWindows).pack(side=TOP, expand=NO, pady=3)
tk.Button(tab2, text='连接设备环境\n修 补', width=12, height=3, command=PatchonDevice).pack(side=TOP, expand=NO, pady=3)
tk.Label(tab2, text='使用设备环境修补不需要\n配置各种参数\n配置来源与设备').pack(side=BOTTOM, expand=NO, pady=3)
tk.Label(tab2, text='选择Magisk版本').pack(side=TOP, expand=NO, pady=3)
comboxlist = ttk.Combobox(tab2, textvariable=mutiseletion, width=14)
comboxlist["values"]=("Magisk-v24.1","Magisk-v24.0","Magisk-v23.0","Magisk-v22.1") 
comboxlist.current(0) # 选择第一个
comboxlist.bind("<<ComboboxSelected>>",select)
comboxlist.pack(side=TOP, expand=NO, pady=3)
tabControl.add(tab2, text='修补')  #把新选项卡增加到Notebook

tab3 = tk.Frame(tabControl)  #增加新选项卡
tk.Button(tab3, text='生成默认配置\nconfig.txt', width=12, height=3, command=GenDefaultConfig).pack(side=TOP, expand=NO, pady=3)
tk.Button(tab3, text='读取设备配置\nconfig.txt', width=12, height=3, command=GetDeviceConfig).pack(side=TOP, expand=NO, pady=3)
tabControl.add(tab3, text='读取')  #把新选项卡增加到Notebook
tab12.pack(side=TOP, expand=NO, fill=BOTH)
tabControl.pack(side=TOP, expand=YES, fill="both")


# Frame 3  信息展示 功能页面
frame3 = LabelFrame(frame2_3, text="信息反馈", labelanchor="nw", relief=SUNKEN, borderwidth=1)
frame3.pack(side=RIGHT, fill=BOTH, padx=2, pady=3, expand=NO)
text = Text(frame3,width=70,height=15)
scroll = Scrollbar(frame3)
scroll.pack(side=RIGHT,fill=Y, padx=1, pady=5)
text.pack(side=RIGHT, expand=YES, fill=BOTH, padx=5 ,pady=1)
scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)
frame2_3.pack(side=TOP, expand=NO, pady=2, fill=BOTH)


# Frame 4 关于 和 清除信息
frame4 = Frame(root, relief=FLAT, borderwidth=1)
tk.Button(frame4, text='清空信息', width=12, height=1, command=cleaninfo).pack(side=RIGHT, expand=NO, pady=3)
tk.Button(frame4, text='关于', width=12, height=1, command=About).pack(side=RIGHT, expand=NO, pady=3)
tk.Button(frame4, text='给我捐钱', width=12, height=1, command=donateme, bg="red", fg="white", font=('黑体', '14')).pack(side=RIGHT, expand=NO, padx=5)
frame4.pack(side=TOP, expand=NO, padx=10, ipady=5, fill=BOTH)

imgLabel = tk.Label(frame4,image=photo)#把图片整合到标签类中
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
text.insert(END,"\n        此脚本为免费工具，如果你花钱买了你就是大傻逼\n")

root.update()
root.mainloop()
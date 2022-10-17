# 欢迎
**中文**｜[English](https://../README_EN.txt)

欢迎使用Magisk Patcher，这是一个基于Python第三方库ttkbootstrap开发的一款能在Windows和Linux上运行的boot修补程序。

 ~~这是affggh为了暴力圈钱写的一款垃圾小工具。虽然钱没圈到多少，不过affggh还是坚持更新了半年。magiskboot从官方源码移植，多次测试十分甚至九分的稳定。~~
 
![GUI Screenshot](bin/gui.png)

## 优势

+ 从magisk官方源码移植，多次测试，稳定性有保障
+ 在多个设备上测试，支持Android 4.3 - 13
+ 在线获取Magisk列表，点击即可下载
+ 可以通过usb调试获取设备修补相关
+ 修复magisk运行环境（待测试）

## 支持系统

**Windows 10, 11 (amd64)**

    如果你在使用32位Windows，请安装Python并运行脚本**而不是**直接运行exe

**Linux**

    已在Ubuntu 20.04 LTS上测试

## 支持被修补的架构

- arm64
- arm
- x86
- x86_64

# 需求

## Windows

在Windows平台运行不需要任何依赖，脚本支持Python 3.8+, 如果你在使用32位系统，请安装Python并运行脚本**而不是**直接运行exe

## Linux

### Debian/Ubuntu:

```bash
sudo apt install python3 python3-tk    
    pip install mttkinter    
    sudo apt install adb # if you need read config from device / 如果你想要读取设备配置
```

### Archlinux:

```bash
yay -S python adb
    pip install mttkinter
```

### 使用Python运行:

```bash
python3 -m pip install ttkbootstrap pillow
python3 ./Magiskpatcher.py
# If you are using ubuntu
sudo apt install python3-pil python3-pil.imagetk
# If you are using arch linux
sudo pacman -S python-pillow
```

**⚠️注意：Batch脚本已被移除，如果你想要使用请下载1.0版本**

# GUI主题
GUI ttk THEME from [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)  

# 感谢

[thka2016](https://github.com/thka2016) 帮我写了个很好用的功能    
[Magisk](https://github.com/topjohnwu/Magisk) 源码来自magisk    

# 捐赠

如果你觉得Magisk Patcher好用可以给我买一瓶水❤️

![](bin/alipay.png)
![](bin/wechat.png)
![](bin/zfbhb.png)

# Magisk_patcher
*Patch boot with magisk on windows  
Batch script support :
                Windows 7 x86_64  
GUI script support   :
                Python 3.7 or newer  
GUI binary support   :
                Windows 10 x86_64  
# GUI screen shortcut
![image](https://github.com/affggh/Magisk_patcher/raw/main/bin/gui.png)
# GUI THEME
GUI ttk THEME from [Sun-Valley-ttk-theme](https://github.com/rdbende/Sun-Valley-ttk-theme)
# Command line Usage:
***
```
  magisk_patcher.bat command
            -h    Print this help information...
  Support Command:
                 patch
                 autoconfig
                 test
  Explain:
         patch  : Patch a boot image with magisk on windows
            -i    input file
 [optional] -o    output file  default output is [new-boot.img]
            -c    read config.txt instead of -a -kv -ke -pv
   [must]   -a    arch of your device... this can be 
                               arm
                               arm64
                               x86
                               x86_64
 [optional] -kv    keep verity default is : [true]
                   If your device is system-as-root(sar)
                       make it true
 [optional] -ke    keep force encrypt default is : [true]
                   If your device is like forceencrypt=footer like [qsee] or else
                       make it true
 [optional] -pv    Patch vbmeta flag default is : [false]
                   If your device not have partition [vbmeta]
                       make it true
 [optional] -m     Choose a Magisk install apk/zip insted of 
                                 default : [prebuilt\magisk.apk]
              Notice: Shell script part will auto detect file existance
                      if is a 64bit image.

         autoconfig : This function can auto detect config from device
                      and generate a confit.txt at D:\cygwin\home\affggh\magiskboot_and_patch_win\MagiskPatcher\ 
                      without root
            --default  generate with default instead read from device
            -m     Defined custom magisk path
        patchondevice : patch on device
                     In some reason patch on windows possibally failed...
                     so we can use device environment to patch...
                     The patch config will follow device instead choose
            -m     Defined custom magisk path

  Example : 
          magisk_patcher.bat patch -i boot.img -c config.txt
          magisk_patcher.bat patch -i boot.img -a armeabi-v7a -kv true -ke true -pv false
          magisk_patcher.bat patch -i boot.img -c config.txt -m prebuilt\magisk.apk

          magisk_patcher.bat autoconfig
          magisk_patcher.bat autoconfig --default
          magisk_patcher.bat autoconfig -m prebuilt\magisk.apk

          magisk_patcher.bat patchondevice -i boot.img -m prebuilt\magisk.apk
```
# General use
***
```
magisk_patcher.bat autoconfig --default
magisk_patcher.bat patch -i boot.img -c config.txt
```
```
magisk_patcher.bat patchondevice -i boot.img -m prebuilt\magisk.apk
```
# Thanks
感谢：    
    [thka2016](https://github.com/thka2016) 帮我写了个很好用的功能    
	[Magisk](https://github.com/topjohnwu/Magisk) 源码来自magisk    

# Donate me
![image](https://github.com/affggh/Magisk_patcher/raw/main/bin/alipay.png)
![image](https://github.com/affggh/Magisk_patcher/raw/main/bin/wechat.png)
![image](https://github.com/affggh/Magisk_patcher/raw/main/bin/zfbhb.png)

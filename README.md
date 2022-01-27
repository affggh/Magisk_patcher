# Magisk_patcher
I've create lots of repositories ,this is the last one...
# Usage:
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

  Example : 
          magisk_patcher.bat patch -i boot.img -c config.txt
          magisk_patcher.bat patch -i boot.img -a armeabi-v7a -kv true -ke true -pv false
          magisk_patcher.bat patch -i boot.img -c config.txt -m prebuilt\magisk.apk

          magisk_patcher.bat autoconfig
          magisk_patcher.bat autoconfig --default
          magisk_patcher.bat autoconfig -m prebuilt\magisk.apk
```
# General use
***
```
magisk_patcher.bat autoconfig --default
magisk_patcher.bat patch -i boot.img -c config.txt
```

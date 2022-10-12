#!/usr/bin/env python3
# 脚本 by affggh
# Apcache 2.0 

import os, sys
import shutil
import subprocess

class Patch:
    def __init__(self, keepverity=True, keepforceencrypt=True, patchvbmetaflag=False, recoverymode=False, debug=False):
        # init defaults
        self.debug = debug
        self.magiskboot = "./magiskboot"
        self.KEEPVERITY = keepverity
        self.KEEPFORCEENCRYPT = keepforceencrypt
        self.PATCHVBMETAFLAG = patchvbmetaflag
        self.RECOVERYMODE = recoverymode
        self.CHROMEOS = False              # Only pixel C need sign with futility
        # self.EXERETURNCODE = 0
        if os.name == 'nt':
            self.creationflags = subprocess.CREATE_NO_WINDOW
        else:
            self.creationflags = 0
        self.env = {
                        'KEEPVERITY': self.bool2str(self.KEEPVERITY),
                        'KEEPFORCEENVRYPT': self.bool2str(self.KEEPFORCEENCRYPT),
                        'PATCHVBMETAFLAG': self.bool2str(self.PATCHVBMETAFLAG),
                        'RECOVERYMODE': self.bool2str(self.RECOVERYMODE)
                    }
        self.setenv()
    
    def setmagiskboot(self, loc):
        self.magiskboot = loc

    def bool2str(self, var):
        if var:
            return "true"
        else:
            return "false"

    def setenv(self):
        '''
        Set environments
        '''
        os.environ['KEEPVERITY'] = self.bool2str(self.KEEPVERITY)
        os.environ['KEEPFORCEENCRYPT'] = self.bool2str(self.KEEPFORCEENCRYPT)
        os.environ['PATCHVBMETAFLAG'] = self.bool2str(self.PATCHVBMETAFLAG)
        os.environ['RECOVERYMODE'] = self.bool2str(self.RECOVERYMODE)
    
    def execv(self, cmd, verbose=False):
        if self.debug:
            print("Debug:")
            print("Run program:", end='')
            print(cmd)
        try:
            ret = subprocess.run(cmd,
                                   shell=False,
                                   #stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   env=self.env,
                                   creationflags=self.creationflags
                                )
        except:
            sys.stderr.write("! Cannot execute program\n")
            return -1
        if self.debug:
            sys.stderr.write(ret.stdout.decode('utf-8'))
        return ret.returncode
    
    def exegetout(self, cmd):
        try:
            ret = subprocess.check_output(cmd,
                                   shell=False,
                                   #stdin=subprocess.PIPE,
                                   #stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   env={
                                          'KEEPVERITY': self.bool2str(self.KEEPVERITY),
                                          'KEEPFORCEENVRYPT': self.bool2str(self.KEEPFORCEENCRYPT),
                                          'PATCHVBMETAFLAG': self.bool2str(self.PATCHVBMETAFLAG),
                                          'RECOVERYMODE': self.bool2str(self.RECOVERYMODE)
                                      },
                                   encoding="utf-8",
                                   creationflags=self.creationflags
                                   )
            return ret
        except:
            return ret
    
    def patchboot(self, infile):

        if not type(infile) == str:
            raise TypeError("infile type must be file path str")

        # unpack boot image
        sys.stdout.write("- Unpacking boot image\n")
        retcode = self.execv([self.magiskboot, "unpack", infile])
        if retcode == 0:
            pass
        elif retcode == 1:
            sys.stderr.write("! Unsupported/Unknown image format\n")
            return False
        elif retcode == 2:
            sys.stdout.write("- ChromeOS boot image detected\n")
            self.CHROMEOS = True
        else:
            sys.stderr.write("! Unable to unpack boot image\n")
            return False
        
        # check ramdisk status
        sys.stdout.write("- Checking ramdisk status\n")
        retcode = self.execv([self.magiskboot, "cpio", "ramdisk.cpio", "test"])
        SHA1 = ""
        if retcode == -1:
            sys.stderr.write("- Error run command Falied !")
            return False
        elif retcode == 0:
            sys.stdout.write("- Stock boot image detected\n")
            SHA1 = self.exegetout([self.magiskboot, "sha1", "%s" %infile])
            shutil.copyfile(infile, "stock-boot.img")
            shutil.copyfile("ramdisk.cpio", "ramdisk.cpio.orig")
        elif retcode == 1:
            sys.stdout.write("- Magisk patched boot image detected\n")
            if os.getenv("SHA1") == "":
                SHA1 = self.exegetout([self.magiskboot, "cpio", "ramdisk.cpio", "sha1"])
            retcode = self.execv([self.magiskboot, "cpio", "ramdisk.cpio", "restore"])
            shutil.copyfile("ramdisk.cpio", "ramdisk.cpio.orig")
            if os.path.isfile("stock-boot.img"):
                os.remove("stock-boot.img")
        elif retcode == 2:
            sys.stderr.write("! Boot image patched by unsupported programs\n",
                             "! Please restore back to stock boot image\n")
            return False
        
        # Work around custom legacy Sony /init -> /(s)bin/init_sony : /init.real setup
        INIT = "init"
        if not retcode&4 == 0:
            INIT = "init.real"
        
        # Ramdisk Patches
        sys.stdout.write("- Patching ramdisk\n")
        with open("config", "w") as f:
            f.write("KEEPVERITY=%s\n" %self.bool2str(self.KEEPVERITY))
            f.write("KEEPFORCEENCRYPT=%s\n" %self.bool2str(self.KEEPFORCEENCRYPT))
            f.write("PATCHVBMETAFLAG=%s\n" %self.bool2str(self.PATCHVBMETAFLAG))
            f.write("RECOVERYMODE=%s\n" %self.bool2str(self.RECOVERYMODE))
            if not SHA1=="":
                f.write("SHA1=%s\n" %SHA1)
        
        skip32 = False
        skip64 = False

        if not os.path.isfile("magisk32"):
            skip32 = True
        else:
            retcode = self.execv([self.magiskboot, "compress=xz", "magisk32", "magisk32.xz"])
        if not os.path.isfile("magisk64"):
            skip64 = True
        else:
            retcode = self.execv([self.magiskboot, "compress=xz", "magisk64", "magisk64.xz"])

        cmd = [self.magiskboot, "cpio", "ramdisk.cpio",
               "add 0750 %s magiskinit" %INIT,
               "mkdir 0750 overlay.d",
               "mkdir 0750 overlay.d/sbin",
               "patch",
               "backup ramdisk.cpio.orig",
               "mkdir 000 .backup",
               "add 000 .backup/.magisk config"]

        if not skip32: cmd.insert(7, "add 0644 overlay.d/sbin/magisk32.xz magisk32.xz")
        if not skip64: cmd.insert(7, "add 0644 overlay.d/sbin/magisk64.xz magisk64.xz")

        retcode = self.execv(cmd)
        os.remove("ramdisk.cpio.orig")
        os.remove("config")
        if os.path.isfile("magisk32.xz"): os.remove("magisk32.xz")
        if os.path.isfile("magisk64.xz"): os.remove("magisk64.xz")

        # Binary Patches
        for dt in ["dtb", "kernel_dtb", "extra"]:
            if os.path.isfile(dt):
                if not self.execv([self.magiskboot, "dtb", dt, "test"]) == 0:
                    sys.stderr.write("! Boot image %s was patched by old (unsupported) Magisk\n" %dt,
                                     "! Please try again with *unpatched* boot image\n")
                    return False
                if self.execv([self.magiskboot, "dtb", dt, "patch"]) == 0:
                    sys.stdout.write("- Patch fstab in boot image %s dt" %dt)
        
        if os.path.isfile("kernel"):
            # Remove Samsung RKP
            retcode = self.execv([self.magiskboot, "hexpatch", "kernel",
                                    "49010054011440B93FA00F71E9000054010840B93FA00F7189000054001840B91FA00F7188010054",
                                    "A1020054011440B93FA00F7140020054010840B93FA00F71E0010054001840B91FA00F7181010054"])
            # Remove Samsung defex
            # Before: [mov w2, #-221]   (-__NR_execve)
            # After:  [mov w2, #-32768]
            retcode = self.execv([self.magiskboot, "hexpatch", "kernel",
                                    "821B8012", "E2FF8F12"])
            # Force kernel to load rootfs
            # skip_initramfs -> want_initramfs
            retcode = self.execv([self.magiskboot, "hexpatch", "kernel",
                                    "736B69705F696E697472616D667300", "77616E745F696E697472616D667300"])
        
        # Repack & Flash
        sys.stdout.write("- Repacking boot image\n")
        if not self.execv([self.magiskboot, "repack", infile]) == 0:
            sys.stderr.write("! Unable to repack boot image\n")
            return False
        
        if self.CHROMEOS:
            sys.stderr.write("- Not support sign with futility on python yet...")
            return False

        return True

if __name__ == '__main__':
    import argparse
    def str2bool(var):
        if var.lower() == "true":
            return True
        else:
            return False
    description = "This python script allow patch boot image on windows/linux with magisk"
    
    parser = argparse.ArgumentParser(prog="boot_patch.py", description=description)

    help = "Keep verity"
    parser.add_argument("-kv", help=help, default="true")

    help = "Keep force encrypt"
    parser.add_argument("-ke", help=help, default="true")

    help = "Patch vbmeta flag"
    parser.add_argument("-pv", help=help, default="false")

    help = "Recovery mode"
    parser.add_argument("-r", help=help, default="false")

    help = "Boot image [Must set]"
    parser.add_argument("BOOTIMG", help=help)

    help = "Debug mode, show more info"
    parser.add_argument("-d", help=help, default="false")
    
    args = parser.parse_args()

    Patch(str2bool(args.kv), 
          str2bool(args.ke), 
          str2bool(args.pv), 
          str2bool(args.r),
          str2bool(args.d)).patchboot(args.BOOTIMG)

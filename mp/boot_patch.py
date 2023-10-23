from sys import stderr
import subprocess
from os import unlink
from os import name as osname
from os.path import isfile, isdir
import logging
from hashlib import sha1
from shutil import copyfile, rmtree

def getsha1(filename):
    with open(filename, 'rb') as f:
        return sha1(f.read()).hexdigest()

def cp(src, dest):
    if isfile(src):
        copyfile(src, dest)

def rm(*files):
    for i in files:
        if isdir(i):
            rmtree(i)
        else:
            if isfile(i):
                unlink(i)

def grep_prop(key, file) -> str:
    with open(file, 'r') as f:
        for i in iter(f.readline, ""):
            if key in i:
                return i.split("=")[1].rstrip("\n")

class BootPatcher(object):
    def __init__(
        self,
        magiskboot,
        keep_verity: bool = True,
        keep_forceencrypt: bool = True,
        patchvbmeta_flag: bool = False,
        recovery_mode: bool = False,
        legacysar: bool = False,
        progress=None,
        log=stderr,
    ):
        self.magiskboot = magiskboot

        self.keep_verity = keep_verity
        self.keep_forceencrypt = keep_forceencrypt
        self.patchvbmeta_flag = patchvbmeta_flag
        self.recovery_mode = recovery_mode
        self.legacysar = legacysar
        self.progress = progress

        self.log = log

        self.__check()
        self.__prepare_env()

    def __check(self):
        if not isfile(self.magiskboot):
            print("- magiskboot文件不存在，无法完成初始化", file=self.log)
            return False

    def __prepare_env(self):
        bool2str = lambda x: "true" if x else "flase"
        self.env = {
            "KEEPVERITY": bool2str(self.keep_verity),
            "KEEPFORCEENCRYPT": bool2str(self.keep_forceencrypt),
            "PATCHVBMETAFLAG": bool2str(self.patchvbmeta_flag),
            "RECOVERYMODE": bool2str(self.recovery_mode),
            "LEGACYSAR": bool2str(self.legacysar),
        }

        # This maybe no need
        #for i in self.env:
        #    putenv(i, self.env[i])
    
    def __execv(self, cmd:list):
        """
        Run magiskboot command, already include magiskboot
        return returncode and output
        """
        full = [
            self.magiskboot,
            *cmd
        ]

        if osname == 'nt':
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0
        logging.info("Run command : \n"+ " ".join(full))
        ret = subprocess.run(full,
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE,
                            shell=False,
                            env=self.env,
                            creationflags=creationflags,
                            )
        logging.info(ret.stdout.decode())
        return ret.returncode, ret.stdout.decode()
    
    def patch(self, bootimg:str) -> bool:
        # Check bootimg exist
        if not isfile(bootimg):
            print("- boot 镜像不存在", file=self.log)
            return False
        
        # Unpack bootimg
        print("- 解包boot镜像...", file=self.log)
        err, ret = self.__execv(["unpack", bootimg])
        logging.info(ret)

        match err:
            case 0: pass
            case 1:
                print("! 不支持/未知 镜像格式", file=self.log)
                return False
            case 2:
                print("- ChromeOS 格式boot镜像", file=self.log)
                print("- 暂不支持")
                return False
            case _:
                print("! 无法解包此boot镜像", file=self.log)
                return False

        print("- 检查ramdisk状态", file=self.log)
        if isfile("ramdisk.cpio"):
            err, ret = self.__execv(["cpio", "ramdisk.cpio", "test"])
            status = err
            skip_backup = ""
        else:
            status = 0
            skip_backup = "#"

        sha = ""
        match (status & 3):
            case 0: # Stock boot
                print("- 检测到原始未修改的boot镜像", file=self.log)
                sha = getsha1(bootimg)
                cp(bootimg, "stock_boot.img")
                cp("ramdisk.cpio", "ramdisk.cpio.orig")
            case 1: # Magisk patched
                print("- 检测到经过magisk修补过的boot镜像", file=self.log)
                err, ret = self.__execv(["cpio", "ramdisk.cpio", "extract .backup/.magisk config.orig", "restore"])
                cp("ramdisk.cpio", "ramdisk.cpio.orig")
                rm("stock_boot.img")
            case 2: # Unsupported
                print("- boot镜像被未知的程序修改过", file=self.log)
                print("- 请先将其还原之原始的boot镜像", file=self.log)
                return False
        
        # Sony device
        init = "init"
        if not (status&4) == 0:
            init = "init.real"
        
        if isfile("config.orig"):
            sha = grep_prop("SHA1", "config.orig")
            rm("config.orig")
        
        print("- 修补ramdisk", file=self.log)

        skip32 = "#"
        skip64 = "#"

        if isfile("magisk64"):
            self.__execv(["compress=xz", "magisk64", "magisk64.xz"])
            skip64 = ""
        if isfile("magisk32"):
            self.__execv(["compress=xz", "magisk32", "magisk32.xz"])
            skip32 = ""
        
        stub = False
        if isfile("stub.apk"):
            stub = True
        
        if stub:
            self.__execv(["compress=xz", "stub.apk", "stub.xz"])
        with open("config", 'w') as config:
            config.write(
                f"KEEPVERITY={self.env["KEEPVERITY"]}" + "\n" +
                f"KEEPFORCEENCRYPT={self.env["KEEPFORCEENCRYPT"]}" + "\n" +
                f"RECOVERYMODE={self.env["RECOVERYMODE"]}" + "\n")
            if sha != "":
                config.write(f"SHA1={sha}\n")
        
        err, _ = self.__execv([
            "cpio", "ramdisk.cpio",
            f"add 0750 {init} magiskinit",
            "mkdir 0750 overlay.d",
            "mkdir 0750 overlay.d/sbin",
            f"{skip32} add 0644 overlay.d/sbin/magisk32.xz magisk32.xz",
            f"{skip64} add 0644 overlay.d/sbin/magisk64.xz magisk64.xz",
            "add 0644 overlay.d/sbin/stub.xz stub.xz" if stub else "",
            "patch",
            f"{skip_backup} backup ramdisk.cpio.orig",
            "mkdir 000 .backup",
            "add 000 .backup/.magisk config",
        ])
        if err != 0:
            print("- 无法修补ramdisk", file=self.log)
            return False
        
        rm("ramdisk.cpio.orig", "config", "magisk32.xz", "magisk64.xz", "stub.xz")
        
        for dt in "dtb", "kernel_dtb", "extra":
            if isfile(dt):
                err, _ = self.__execv([
                    "dtb", dt, "test"
                ])
                if err != 0:
                    print(f"- Boot 镜像中的{dt}被旧的magisk修补过", file=self.log)
                    print("- 请使用没有修改过的boot镜像再试一次", file=self.log)
                    return False
                err, _ = self.__execv([
                    "dtb", dt, "patch"
                ])
                if err == 0:
                    print(f"- 修补boot镜像中{dt}的fstab")
        
        if isfile("kernel"):
            patchedkernel = False
            err, _ = self.__execv([
                "hexpatch", "kernel",
                "49010054011440B93FA00F71E9000054010840B93FA00F7189000054001840B91FA00F7188010054",
                "A1020054011440B93FA00F7140020054010840B93FA00F71E0010054001840B91FA00F7181010054"
            ])
            if err == 0: patchedkernel = True
            err, _ = self.__execv([
                "hexpatch", "kernel", "821B8012", "E2FF8F12"
            ])
            if err == 0: patchedkernel = True
            if self.legacysar:
                err, _ = self.__execv([
                    "hexpatch", "kernel",
                    "736B69705F696E697472616D667300",
                    "77616E745F696E697472616D667300"
                ])
                if err == 0: patchedkernel = True
            if not patchedkernel: rm("kernel")

        print("- 打包boot镜像", file=self.log)
        err, _ = self.__execv([
            "repack", bootimg
        ])
        if err != 0:
            print("- 打包boot镜像失败", file=self.log)
            return False

        self.cleanup()
        print("- 完成！", file=self.log)
        return True

    def cleanup(self):
        rmlist = [
        "magisk32", "magisk32.xz", "magisk64", "magisk64.xz", "magiskinit", "stub.apk"
        ]
        rm(*rmlist)
        print("- 清理文件", file=self.log)
        self.__execv(["cleanup"])

if __name__ == "__main__":
    print(grep_prop("B", "config"))

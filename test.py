import os
import shutil
import zipfile

arch = "arm64"

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
        False
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
        print("Parse Magisk Version : " + mVersion)
        for i in tl:
            if arch == "arm64":
                if i.startswith("lib/arm64-v8a/") and i.endswith(".so"):
                    if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                        f.extract(i, "tmp")
            elif arch == "arm":
                if i.startswith("lib/armeabi-v7a/") and i.endwith(".so"):
                    if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                        f.extract(i, "tmp")
            elif arch == "x86_64":
                if i.startswith("lib/x86_64/") and i.endwith(".so"):
                    if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                        f.extract(i, "tmp")
            elif arch == "x86":
                if i.startswith("lib/x86/") and i.endwith(".so"):
                    if not (i.endswith("busybox.so") or i.endswith("magiskboot.so")):
                        f.extract(i, "tmp")
        for i in tl:
            if arch == "arm64" and not os.access("libmagisk32.so", os.F_OK):
                if i == "lib/armeabi-v7a/libmagisk32.so":
                    f.extract("lib/armeabi-v7a/libmagisk32.so", "tmp")
            elif arch == "x86_64" and not os.access("libmagisk32.so", os.F_OK):
                if i == "lib/x86/libmagisk32.so":
                    f.extract("lib/armeabi-v7a/libmagisk32.so", "tmp")
        for root, dirs, files in os.walk("tmp"):
            for file in files:
                if file.endswith(".so"):
                    shutil.move(root+os.sep+file, rename(os.path.basename(file)))
        shutil.rmtree("tmp")


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

if __name__ == '__main__':
    parseZip("./prebuilt/Magisk-v24.3.apk")
    cleanUp()
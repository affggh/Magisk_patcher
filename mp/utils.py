from os import name as osname
from sys import stderr
import subprocess
import requests
import zipfile
from multiprocessing.dummy import DummyProcess
import platform
from os import chmod

DEFAULT_MAGISK_API_URL = "https://api.github.com/repos/topjohnwu/Magisk/releases"
DELTA_MAGISK_API_URL = "https://api.github.com/repos/HuskyDG/magisk-files/releases"

def retTypeAndMachine():
    # Detect machine and ostype
    ostype = platform.system().lower()
    if ostype.find("cygwin") >= 0:  # Support cygwin x11
        ostype = "windows"
    machine = platform.machine().lower()
    if machine == 'aarch64_be' \
        or machine == 'armv8b' \
        or machine == 'armv8l':
        machine = 'aarch64'
    if machine == 'i386' or machine == 'i686':
        machine = 'x86'
    if machine == "amd64":
        machine = 'x86_64'
    return ostype, machine

def runcmd(cmd):
    if osname == 'posix':
        creationflags = 0
    elif osname == 'nt':  # if on windows ,create a process with hidden console
        creationflags = subprocess.CREATE_NO_WINDOW
    else:
        creationflags = 0
    ret = subprocess.run(cmd,
                                   shell=False,
                                   #stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   creationflags=creationflags
                                )
    return (ret.returncode, ret.stdout.decode('utf-8'))

def getReleaseList(url: str = DEFAULT_MAGISK_API_URL, isproxy: bool=False, proxyaddr: str="127.0.0.1:7890", isjsdelivr:bool=True, log=stderr):
    buf = url.split('/')
    user = buf[-3]
    repo = buf[-2]

    proxies = {
        'http': f"{proxyaddr}",
        'https': f"{proxyaddr}",
    }
    r = requests.get(url,
                     proxies=proxies if isproxy else None,
                     timeout=3)
    if not r.ok:
        print("获取版本失败，请检查网络或尝试添加代理...", file=log)
        return {}
    data = r.json()
    dlink = {}

    if url == DEFAULT_MAGISK_API_URL:
        for i in data:
            tag_name = i['tag_name']
            for j in i['assets']:
                if j['name'].startswith("Magisk") and j['name'].endswith(r".apk"):
                    if "Manager" in j['name']: continue # skip magisk manager apk
                    if isjsdelivr:
                        dlink.update({j['name'] : magiskTag2jsdelivr(user, repo, tag_name, j['name'])})
                    else:
                        dlink.update({j['name'] : j['browser_download_url']})
    else: # maybe delta magisk
        for i in data:
            tag_name = i['tag_name']
            for j in i['assets']:
                if j['name'].endswith(r".apk") and j['name'].startswith('app'):
                    if isjsdelivr:
                        dlink.update({tag_name + j['name'].lstrip('app') : magiskTag2jsdelivr(user, repo, tag_name, j['name'])})
                    else:
                        dlink.update({tag_name + j['name'].lstrip('app') : j['browser_download_url']})
    return dlink

def magiskTag2jsdelivr(user, repo, tag, fname):
    '''
    input link and tag get jsdilivr link
    '''
    if user == "topjohnwu": # official magisk
        return f"https://cdn.jsdelivr.net/gh/{user}/magisk-files@{tag.lstrip('v')}/app-release.apk"
    return f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{tag}/{fname}"

def getMagiskApkVersion(fname: str) -> str | None:
    '''
    Give magisk apk file and return version code
    '''
    valid_flag = False
    magisk_ver_code = "00000"
    with zipfile.ZipFile(fname, 'r') as z:
        for i in z.filelist:
            if "util_functions.sh" in i.filename:
                valid_flag = True
                for line in z.read(i).splitlines():
                    if b"MAGISK_VER_CODE" in line:
                        magisk_ver_code = line.split(b"=")[1]
        if not valid_flag: return None
    return magisk_ver_code

def convertVercode2Ver(value: str) -> str:
    return value[0:2] + b"." + value[2:3]

def downloadFile(url: str, to: str, isproxy: bool = False, proxy:str="127.0.0.1:7890", progress=None, log=stderr):
    """
    Can accept a ttk.ProgressBar as progress
    """
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    p = lambda now, total: int((now/total)*100)
    chunk_size = 10240
    try:
        r = requests.get(url, stream=True, allow_redirects=True,
                         proxies=proxies if isproxy else None)
    except:
        print("- 网络异常或无法连接到目标链接...", file=log)
        return False
    print("- 开始下载[%s] -> [%s]" %(url, to), file=log)
    total_size = int(r.headers['content-length'])
    now = 0
    with open(to, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                before = now
                f.write(chunk)
                now += chunk_size
                if now > before:
                    progress.set(p(now, total_size))
    print("- 下载完成", file=log)
    progress.set(0)
    return True

def thdownloadFile(*args):
    dp = DummyProcess(target=downloadFile, args=[*args, ])
    dp.start()

def parseMagiskApk(apk: str, arch:["arm64", "arm", "x86", "x86_64"]="arm64", log=stderr):
    """
    This function will extract useful file from magisk.apk
    """
    def archconv(a):
        ret = a
        match a:
            case "arm64":
                ret = "arm64-v8a"
            case "arm":
                ret = "armeabi-v7a"
        return ret
    
    def archto32(a):
        ret = a
        match a:
            case "arm64-v8a":
                ret = "armeabi-v7a"
            case "x86_64":
                ret = "x86"
        return ret

    def saveto(bytes, path):
        with open(path, 'wb') as f:
            f.write(bytes)

    print("- 开始解压需要的文件...", file=log)
    arch = archconv(arch)
    os, p = retTypeAndMachine()
    pp = "x86_64"
    if p == "aarch64":
        pp = "arm64-v8a"
    elif p == "arm":
        pp = "armeabi-v7a"
    with zipfile.ZipFile(apk) as z:
        for l in z.filelist:
            # 26.0+
            if "stub.apk" in l.filename:
                saveto(z.read(l), "stub.apk")
            # Save a platform magiskboot into bin if linux
            if os!='windows' and osname !='nt':
                if f"lib/{pp}/libmagiskboot.so" in l.filename:
                    saveto(z.read(l), "bin/magiskboot")
                    chmod("bin/magiskboot", 0o755)

            if f"lib/{arch}/libmagiskinit.so" in l.filename:
                saveto(z.read(f"lib/{archto32(arch)}/libmagisk32.so"), "magisk32")
                if arch in ["arm64-v8a", "x86_64"]:
                    saveto(z.read(f"lib/{arch}/libmagisk64.so"), "magisk64")
                saveto(z.read(f"lib/{arch}/libmagiskinit.so"), "magiskinit")

if __name__ == '__main__':
    print(getReleaseList(url=DELTA_MAGISK_API_URL))

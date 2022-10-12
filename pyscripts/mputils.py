import threading
import time, sys, os
import subprocess
import requests

def runcmd(cmd):
    if os.name == 'posix':
        creationflags = 0
    elif os.name == 'nt':  # if on windows ,create a process with hidden console
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
    print(ret.stdout.decode('utf-8'))
    return (ret.returncode, ret.stdout.decode('utf-8'))

def retCurrentTime():
    return time.strftime('%H:%M:%S')

def getReleaseList(GitUrl):
    if type(GitUrl) != str:
        raise TypeError("GitUrl must be a str type")
    try:
        data = requests.get(GitUrl).json()
    except:
        sys.stderr.write("通过github的api获取magisk版本失败...\n请检查网络连接...\n使用代理上网更容易获取列表...\n")
        return {}
    dlink = {}
    for i in data:
        for j in i['assets']:
            if j['name'].startswith("Magisk-v") and j['name'].endswith(".apk"):
                dlink.update({j['name'] : j['browser_download_url']})
    return dlink

def magiskVresion2jsdelivr(ver):
    '''
    input Magisk-v22.5 return jsdelivr download link
    '''
    ver = ver.strip("Magisk-v")
    return "https://cdn.jsdelivr.net/gh/topjohnwu/magisk-files@%s/app-release.apk" %ver



if __name__ == '__main__':
    print(getReleaseList("https://api.github.com/repos/topjohnwu/Magisk/releases"))
import time, sys
import requests

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

if __name__ == '__main__':
    print(getReleaseList("https://api.github.com/repos/topjohnwu/Magisk/releases"))
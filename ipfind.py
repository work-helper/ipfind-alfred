# -*- coding: utf-8 -*-
import json
import socket
import string
import sys
import urllib.request

ipRest = "https://api.ttt.sh/ip/qqwry/"


# 查询外网ip
def findNetIp(ip=''):
    urlopen = urllib.request.urlopen(ipRest + ip, timeout=2000)
    resp = urlopen.read().decode('utf-8')
    body = json.loads(resp)
    return body['address'], body['ip']


# 获取本地ip信息
def findLocalIp():
    global s
    hostname = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
        return hostname, ip
    finally:
        s.close()

if __name__ == '__main__':
    argLength = len(sys.argv)
    ip = ''
    if argLength != 1:
        ip = sys.argv[1]

    result = '''
{
    "items": [{
        "uid": "1",
        "title": "LocalHost  -->  $localIp",
        "subtitle": "$localHostname",
        "arg": "$localIp",
        "icon": {
            "path": "./icon.png"
        }
    },
    {
        "uid": "2",
        "title": "NetHost  -->  $netIp",
        "subtitle": "$netHostname",
        "arg": "$netIp",
        "icon": {
            "path": "./icon.png"
        }
    }]
}
    '''
    # 拿到IP地址
    localHostname, localIp = findLocalIp()
    netHostname, netIp = findNetIp(ip)

    template = string.Template(result)
    print(template.substitute(localIp=localIp, localHostname=localHostname, netHostname=netHostname, netIp=netIp))

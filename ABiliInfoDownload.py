import os
import sys
import time

from selenium.webdriver.common.by import By
import requests

import BUtils
import MyUtils

UserUID = ''


def Download():
    global page
    url = (f'https://api.bilibili.com/x/space/arc/search?mid={UserUID}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp')
    res = requests.get(url, headers=MyUtils.headers)
    if page*30 > res.json()['data']['page']['count'] and not page==1:
        return
    page += 1
    for video in res.json()['data']['list']['vlist']:
        aid = video['aid']
        bvid = video['bvid']
        UserID=MyUtils.MyName(video["author"])
        title = MyUtils.MyName(video['title'])

        if not os.path.exists(f'../bili/{UserID}_{UserUID}/{title}_{bvid}'):
            continue

        description = (video['description'])
        f=MyUtils.txt(f'../bili/{UserID}_{UserUID}/{title}_{bvid}/简介.txt')
        f.add(description)
        f.save()
        if (os.path.exists(f'../bili/{UserID}_{UserUID}/{title}_{bvid}/cover.jpg')):
            continue
        MyUtils.requestdownload(f'../bili/cover/{UserID}/{title}_{bvid}/cover.jpg', 'wb', video['pic'])
        print(f'视频信息下载完成{UserID}-{title}')
    Download()


coverspectrum=MyUtils.RefreshTXT('D:/Kaleidoscope/bili/CoverSpectrum.txt')
BUtils.AddUser('https://space.bilibili.com/661654199/fans/follow?tagid=402237', coverspectrum)



while True:
    UserUID=coverspectrum.get()
    if UserUID==None:
        sys.exit()
    page=1
    print(f'[Main]用户总数 {coverspectrum.loopcount}/{coverspectrum.length()}')
    Download()
    coverspectrum.save()
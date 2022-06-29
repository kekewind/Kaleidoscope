import sys
import time
import pyautogui
import requests

import BUtils
import MyUtils
import pyperclip

MAX=10
count=0

def Download():
    global page, VideoSpectrum, UserUID, UserSpectrum,count,MAX
    # 根据视频时长设置等待下载时间
    tim=0
    # 获取Bv号
    url = (f'https://api.bilibili.com/x/space/arc/search?mid={UserUID}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp')
    res = requests.get(url, headers=MyUtils.headers)
    # 如果结束就退出
    if page * 30 > res.json()['data']['page']['count'] and not page == 1:
        return
    # 获取一页的全部BVid
    vlist = []
    for a in res.json()['data']['list']['vlist']:
        vlist.append(a['bvid'])
        tttt=a['length']
        tim+=int(tttt[:tttt.find(':')])
    for bvid in vlist:
        print(f'{MyUtils.MyTime("hms")}[Main] 已汇入下载器{bvid} {UserUID}')
        if not VideoSpectrum.exist(bvid):
            #     如果未下载过
            # 如果是合集
            if vlist.count(bvid) > 3:
                time.sleep(20)
                sss=input()
                print('is waited')
            if vlist.count(bvid) > 6:
                time.sleep(20)
            if vlist.count(bvid) > 9:
                time.sleep(40)
            if vlist.count(bvid) > 15:
                time.sleep(100)
            #     下载
            # 生成网址
            pyperclip.copy(f'https://www.bilibili.com/video/{bvid}')
            time.sleep(5)
            #     点击下载
            # pyautogui.click(305, 985)+
            time.sleep(5)
            # pyautogui.click(1594, 985)

            # 认为下载完成
            count+=1
            if count>MAX:
                time.sleep(10)

    # 本页下载完了，下一页
    # time.sleep(tim*2)
    tim=0
    page += 1
    Download()


UserSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoUserSpectrum.txt')
BUtils.AddUser('https://space.bilibili.com/661654199/fans/follow?tagid=402237',UserSpectrum)
VideoSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoSpectrum.txt')
# 转到软件
# pyautogui.hotkey('alt', 'tab')
time.sleep(1)
while UserSpectrum.loopcount < UserSpectrum.length():
    UserUID = UserSpectrum.get()
    UserSpectrum.save()
    page = 1
    Download()

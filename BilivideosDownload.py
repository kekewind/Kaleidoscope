import sys
import time
import pyautogui
import requests
from retrying import retry

import BUtils
import MyUtils
import pyperclip

MAX = 12
count = 0




def detect(UserUID):
    res = BUtils.hostjson(UserUID, page)
    while res == None:
        res = BUtils.hostjson(UserUID, page)
        MyUtils.warn('重新获取元数据中...')
        time.sleep(5)
    return res.json()


def download():
    c=readytodownload.get()
    vlist=MyUtils.value(c)
    for bvid in vlist:
        if BUtils.skipdownloaded(bvid):
            continue
        pyperclip.copy(f'https://www.bilibili.com/video/{bvid}')
        MyUtils.click(1449, 214)
        time.sleep(0.7)
        MyUtils.click(988, 500)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.7)
        pyautogui.hotkey('enter')
        time.sleep(5)

        MyUtils.click(708, 504)
        time.sleep(0.7)
        MyUtils.click(1208, 576)
        time.sleep(0.7)
        MyUtils.click(1246, 722)
        time.sleep(0.7)

        # count += 1
        # if count > MAX:
        #     UserSpectrum.rollback()
        #     MyUtils.warn(f'达到最大下载个数{MAX}')
        #     sys.exit(-1)


page = 1
VideoSpectrum = BUtils.videospectrum
UserSpectrum = BUtils.videouserspectrum
readytodownload=BUtils.readytodownload
count = 0
MAX = 9999
useruid = ''
cachepath = './bili/cache'

# 添加新的用户
def step0():
    BUtils.addwebuser()

# step0()


@retry(retry_on_exception=MyUtils.retry)
def main():
    vlist = []
    # 准备工作 - 检查为空，添加下载列表
    def step1():
        def checkempty():
            if not [] == MyUtils.listdir(cachepath):
                pyperclip.copy(MyUtils.standarlizedPath(cachepath))
                MyUtils.Exit('cache不为空。')
        checkempty()
        user=UserSpectrum.get()[0]
        useruid = MyUtils.key(user)
        res = detect(useruid)

        # 获取json中的量
        for a in res['data']['list']['vlist']:
            vlist.append(a['bvid'])
        readytodownload.add({useruid:vlist})
        readytodownload.add({useruid:vlist})

    # 使用下载器下载
    def step2():
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.3)
        download()
        pyautogui.hotkey('alt', 'tab')

    # 等待下载完毕后转移文件
    def step3():
        useruid=MyUtils.key(MyUtils.jsontodict(readytodownload.get()))
        # useruid='4441160'
        for i in MyUtils.listdir('./bili/cache'):
            # 如果里面有.m4s文件就跳过
            b=True
            for j in MyUtils.listfile(i):
                if '.m4s'in j:
                    b=False
                    MyUtils.deletedirandfile([i])
            if not b:
                continue
            j = MyUtils.filename(i)
            j = MyUtils.removetail(j, '-')
            j, bvid = MyUtils.cuttail(j, '-')
            title, author = MyUtils.cuttail(j, '-')
            MyUtils.move(i, f'./bili/{author}_{useruid}/{title}_{bvid}')

    step1()
    step2()
    # 等待下载完毕
    big=0
    while True:
        newbig=MyUtils.size('./bili/cache')
        print(newbig)
        if newbig==big:
            break
        big=newbig
        time.sleep(20)
    step3()

if __name__ == '__main__':
    while True:
        main()
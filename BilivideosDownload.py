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


def checkempty():
    if not [] == MyUtils.listdir(cachepath):
        MyUtils.warn('cache不为空。')
        pyperclip.copy(MyUtils.standarlizedPath(cachepath))
        sys.exit(-1)


def detect(UserUID):
    res = BUtils.hostjson(UserUID, page)
    while res == None:
        res = BUtils.hostjson(UserUID, page)
        MyUtils.warn('重新获取元数据中...')
        time.sleep(5)
    return res.json()


def download(vlist):
    for bvid in vlist:
        MyUtils.log(f'{bvid}   -用户{useruid}')
        if BUtils.skipdownloaded(bvid):
            continue
        pyperclip.copy(f'https://www.bilibili.com/video/{bvid}')
        pyautogui.click(1449, 214)
        time.sleep(0.5)
        pyautogui.click(988, 500)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        time.sleep(2)

        pyautogui.click(708, 504)
        time.sleep(0.5)
        pyautogui.click(1208, 576)
        time.sleep(0.5)
        pyautogui.click(1246, 722)

        # count += 1
        # if count > MAX:
        #     UserSpectrum.rollback()
        #     MyUtils.warn(f'达到最大下载个数{MAX}')
        #     sys.exit(-1)


page = 1
VideoSpectrum = BUtils.videospectrum
UserSpectrum = BUtils.videouserspectrum
currentuser = MyUtils.cache('./bili/CurrentUser.txt')
count = 0
MAX = 9999
useruid = ''
cachepath = './bili/cache'


def step0():
    BUtils.addwebuser()
    pyautogui.hotkey('alt', 'tab')


step0()


@retry(retry_on_exception=MyUtils.retry)
def main():
    def step1():
        checkempty()
        user = UserSpectrum.get()[0]
        useruid = MyUtils.key(user)
        currentuser.add(user)
        res = detect(useruid)

        # 获取json中的量
        vlist = []
        for a in res['data']['list']['vlist']:
            vlist.append(a['bvid'])
            # tttt = a['length']
            # tim += int(tttt[:tttt.find(':')])

        download(vlist)

    def step2():
        pass

    def step3():
        user = currentuser.get()
        if user == None:
            MyUtils.warn(f'{currentuser.path}可能为空')
            sys.exit(-1)
        uid = MyUtils.key(user)
        for i in MyUtils.listdir('./bili/cache'):
            j = MyUtils.filename(i)
            j, what = MyUtils.cuttail([j], '-')
            j, bvid = MyUtils.cuttail([j], '-')
            title, author = MyUtils.cuttail([j], '-')
            MyUtils.move(i, f'./bili/{author}_{uid}/{title}_{bvid}')

    # step1()
    # step2()
    step3()


if __name__ == '__main__':
    main()

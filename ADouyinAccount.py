import re
import sys
import time

import pyautogui
import pyperclip
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import MyUtils

# 初始化
LocalUserSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
LocalVideoSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/VideoSpectrum.txt')
print('Account Like processing. LocalVideo: ', (LocalVideoSpectrum.length()), ' LocalUser: ', (LocalUserSpectrum.length()))
# 定义字典
likecount={}

try:
    # 登录
    page = MyUtils.MyEdge('https://www.douyin.com/user/MS4wLjABAAAAPw9P0loZpA5wjaWiHzxQb4B9E2Jgt4ZPWfiycyO_E4Q')
    time.sleep(3)
    MyUtils.MySkip([page, By.ID, "captcha-verify-image"])
    MyUtils.MySkip([page, By.ID, "login-pannel"])
    time.sleep(3)

    # 转到喜欢页面
    # page.get(MyUtils.MyElement([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/user/")]']).get_attribute('href'))
    # time.sleep(1)
    LikeElement=MyUtils.MyElement([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[2]/span'])
    LikeNum=LikeElement.text
    LikeElement.click()

    # 下滚，保存列表
    time.sleep(2)
    MyUtils.MyScroll([page])
    WebUserSpectrum = []
    VideoList=[]
    for VideoElement in MyUtils.MyElements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/video/")]']):
        VideoUrl = VideoElement.get_attribute('href')
        VideoNum = VideoUrl[29:len(VideoUrl)]
        VideoList.append(VideoNum)

    # 逐一打开
    for VideoNum in VideoList:
        # 转到Video页面，没下过的第一遍进WebUserSpectrum
        page.get(f'https://www.douyin.com/video/{VideoNum}')
        time.sleep(2)


        # 跳过验证
        MyUtils.MySkip([page, By.ID, "captcha-verify-image"])

        # 跳过直播
        UserUrl=MyUtils.MyElement([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/a']).get_attribute('href')
        if UserUrl.rfind('live')>0:
            continue

        # 获取UserUID
        UserUID=UserUrl[UserUrl.rfind('/')+1:]
        # LocalUserSpectrum.add(UserUID)

        # 取消喜欢
        MyUtils.MyClick([page, By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div[1]'])
        time.sleep(2)

        # # 跳过UserUID已经记录的
        # if (UserUID in LocalUserSpectrum.l):
        #     continue

        # 跳过下载过的
        if (VideoNum in LocalVideoSpectrum.l):
            print(f'[Main] 已下载，在记录中.{VideoNum}')
            continue

        # 获取title
        title = MyUtils.MyElement([page, By.XPATH, '//head/title[1]']).get_attribute('text')
        title = title[0:len(title) - 5]
        title = MyUtils.MyName(title)

        # 获取UserID
        s = MyUtils.MyElement([page, By.XPATH, '/html/head/meta[3]']).get_attribute('content')
        UserID = s[s.rfind(' - ') + 3:s.rfind('发布在抖音，已经收获了') - 9]

        # 下载
        VideoUrl = MyUtils.MyElement([page, By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-video-container/video/source[1]']).get_attribute(
            'src')
        path = '../抖音/' + UserID
        MyUtils.MyCreatePath(path)
        MyUtils.MyRequestDownload(f'{path}/{title}.mp4','wb',VideoUrl)
        LocalVideoSpectrum.add(VideoNum)
        print(f'[抖音] {UserID}-{title}  下载完成，添加记录完成（安全）。')
        print(f'{VideoUrl}')

    #     查看是否需要记录UserUID
        if likecount.get(UserUID)==None:
            likecount.update({UserUID:1})
            print('[Main]添加了新用户')
        else:
            likecount.update({UserUID:likecount.get(UserUID)+1})
            print('[Main]已经出现过的用户')
            if likecount.get(UserUID)>1:
                likecount.update({UserUID:0})
                print('[Main]记录了新用户')
                LocalUserSpectrum.add(UserUID)

        print(likecount)
    # 结束
    page.quit()

finally:
    LocalVideoSpectrum.save()
    LocalUserSpectrum.save()

sys.exit(0)

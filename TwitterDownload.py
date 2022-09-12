import os.path
import re
import time

import pyperclip
import pyautogui
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

import MyUtils

TwitterSum = 0
TotalExceptionNum = 0
headers = MyUtils.headers

LocalUserSpectrum = MyUtils.file('r', './twitter/AllUsers.txt')
LocalContentSpectrum = MyUtils.file('r', './twitter/ContentSpectrum.txt')
LocalPictureSpectrum = MyUtils.file('r', './twitter/PictureSpectrum.txt')

page = MyUtils.chrome()
# 遍历用户序列
for UserUID in LocalUserSpectrum:
    UserUID=LocalUserSpectrum.pop(0)
    LocalUserSpectrum.append(UserUID)
    UserUID = MyUtils.MyName(UserUID[0:len(UserUID) - 1])
    page.get('https://www.twitter.com/' + UserUID)
    page.set_window_size(400, 1000)
    time.sleep(3)
    UserID = MyUtils.MyTitle([page])[MyUtils.MyTitle([page]).find(')') + 2:MyUtils.MyTitle([page]).rfind(UserUID) - 3]
    ScrollTop = -1

    # 保存封面
    MyUtils.file('wb', f'./twitter/{UserUID}/cover/{UserID}\
    {time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}.png', \
                 MyUtils.Element([page, By.XPATH,\
            '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div']).screenshot_as_png)

    # 不断下滚
    height=-1
    while MyUtils.getscrolltop([page])>height:
        height=MyUtils.getscrolltop([page])
        time.sleep(2)
        MyUtils.setscrolltop([page, height])
        WebContentSpectrum = page.find_elements(By.XPATH, '//div[starts-with(@style,"transform:")]')
        # 遍历所有tweet
        for content in WebContentSpectrum:
            # 滚动到每个tweet，0编号保存截图，找不到则进入下一个WebContentSpectrum
            if not WebContentSpectrum[0]==page.find_elements(By.XPATH, '//div[starts-with(@style,"transform:")]')[0]:
                break
            if MyUtils.getscrolltop([page])>=content.csv_f['y'] - 53:
                continue
            MyUtils.setscrolltop([page, content.csv_f['y'] - 53])
            if content.text.rfind(UserUID) < 0 and content.text.rfind(UserID) < 0 or content.text.rfind('etweet') > 0 or content.text.rfind('ollow') > 0:
                continue
            Name=(MyUtils.Element([content, By.XPATH, './/div[@lang]/span'], 7))
            if not Name==None:
                Name=MyUtils.MyName(Name.text)
            else:
                Name=' '
            if os.path.exists(f'./twitter/{UserUID}/tweets/{Name}.png'):
                if os.path.getsize(f'./twitter/{UserUID}/tweets/{Name}.png')>1:
                    continue
            MyUtils.file('wb', f'./twitter/{UserUID}/tweets/{Name}.png', content.screenshot_as_png)
            # 保存每个tweet里的图片，123开始标序，文案作为文件名
            i=0
            for pic in MyUtils.Elements([content, By.XPATH, './/img']):
                # 跳过第一个不标
                if i == 0:
                    i+=1
                    continue
                # 处理链接
                pic = pic.get_attribute('src')
                pic = re.sub('name=[1-9][0-9]*x[1-9][0-9]*', 'name=large', pic)
                pic = re.sub('name=small', 'name=large', pic)
                if pic + '\n' in LocalPictureSpectrum:
                    continue
                # 下载图片
                LocalPictureSpectrum.append(pic+'\n')
                MyUtils.pagedownload(pic, f'./twitter/{UserUID}/Pic/{Name}No.{i}.png')
                i+=1
            print(f'Done-文案：{Name}')

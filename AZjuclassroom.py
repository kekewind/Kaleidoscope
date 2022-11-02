import os.path
import sys
import time

from selenium.webdriver.common.by import By

import MyUtils

# 打开主网页，获取信息
txt = MyUtils.RefreshTXT('../浙江大学课堂/cache.txt')
page = MyUtils.chrome(mine=True)
result = []
while True:
    URL = txt.get()
    print('[Main] Processing', URL)
    if URL == None:
        break
    page.get(URL)
    Lecture = MyUtils.title([page])
    Teacher = MyUtils.Element([page, By.XPATH, '/html/body/main/section/div[1]/div/div[2]']).text.strip("发布教师：")
    Spectrum = MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"https://classroom")]'])

    # 检查是否已经全部保存
    All = MyUtils.Elements([page, By.XPATH, '/html/body/main/section/div[2]/div/div/div/ul/li/ul/li'])
    MyUtils.CreatePath(f'../浙江大学课堂/{Lecture}{Teacher}')
    number = 0
    for (root, dirs, files) in os.walk(f'../浙江大学课堂/{Lecture}{Teacher}'):
        number = len(files)
        break
    if number == len(All):
        print('[Main]检测到该课程已结束并且在本地已经全部下载，跳过。')
        continue

    # 保存链接表
    urlList = []
    for i in Spectrum:
        urlList.append(i.get_attribute('href'))

    # 依次在原页面打开，下载
    for url in urlList:
        page.get(url)
        time.sleep(5)
        title = '智云课堂'
        while title.find('云课堂') > 0:
            title = MyUtils.title([page])
        result.append(title)
        if not os.path.exists(f'../浙江大学课堂/{Lecture}{Teacher}/{title}.mp4'):
            print(f"Downloading{title}")
            MyUtils.requestdownload(f'../浙江大学课堂/{Lecture}{Teacher}/{MyUtils.title([page])}.mp4', 'wb', MyUtils.Element(
                [page, By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/video']).get_attribute('src'))
            print('Download complete.')

print(result)

import time

import MyUtils
import pyautogui
import selenium.webdriver
from selenium.webdriver.common.by import By

# 进入，获取回答列表
page=MyUtils.MyChrome('https://www.zhihu.com/collection/791721748',silent=None,mine=True)
time.sleep(2)
StarredList=MyUtils.MyElements([page,By.XPATH,'/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div'])
for i in StarredList:

    # 展开
    MyUtils.MyClick([page,By.XPATH,'/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/button'])
    time.sleep(3)

    # 截屏
    page.set_window_size(800, 2000+i.size['height'])
    MyUtils.MyScreenShot([i,f'../知乎/收藏/{MyUtils.MyName(i.text)}.png'])
    time.sleep(2)

    # 完毕，取消收藏
    MyUtils.MySetScrollTop([page,i.size['height']])
    MyUtils.MyClick([page,By.XPATH,'/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[4]/button[2]'])
    # 刷新
    page.refresh()
    time.sleep(3)
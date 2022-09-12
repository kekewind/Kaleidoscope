import os
import time

import MyUtils
import pyautogui
import selenium.webdriver
from selenium.webdriver.common.by import By

# page=MyUtils.chrome('https://www.zhihu.com/collection/791721748', silent=True,mine=True)
page=MyUtils.chrome('https://www.zhihu.com/collection/791721748', silent=None,mine=True)
# page=MyUtils.chrome('https://www.zhihu.com/collection/782323705', silent=True,mine=True)
# MyUtils.skip([page,By.XPATH,'/html/body/div[1]/div/div[4]/div[1]/div[1]/a'])
time.sleep(2)

while True:
    # 展开
    # MyUtils.MyClick([page,By.XPATH,'/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/button'])
    MyUtils.click([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/span/div/button'])
    time.sleep(2)

    # 获取变量
    Answer=MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div'])
    te=Answer.text
    title=MyUtils.standarlizedFile(te[:80])
    # StarredList=MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div'])

    # 保存文本
    if not os.path.exists(f'./知乎/plaintext/{title}.txt'):
        MyUtils.txt(f'./知乎/plaintext/{title}').add(te)

    # 截屏
    # answer=MyUtils.Element[page,By.CLASS_NAME,'CollectionDetailPageItem-innerContainer']
    page.set_window_size(800, 2000+Answer.size['height'])
    MyUtils.scrshot([Answer,(f'./知乎/{title}.png')])
    # MyUtils.MyScreenShot([i,f'./知乎/收藏/{MyUtils.MyName(i.text)}.png'])
    time.sleep(2)

    # 完毕，取消收藏
    MyUtils.setscrolltop([page, 0])
    MyUtils.click([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[3]/div/button[2]'])
    page.refresh()
    time.sleep(2)
    MyUtils.log(f'已保存回答、：{title}')
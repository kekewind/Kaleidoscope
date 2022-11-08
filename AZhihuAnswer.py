import os
import time

import MyUtils
import pyautogui
import selenium.webdriver
from selenium.webdriver.common.by import By

Aurl = 'https://www.zhihu.com/collection/782323705'
# page=MyUtils.chrome('https://www.zhihu.com/collection/791721748', silent=True,mine=True)
# page = MyUtils.Chrome('https://www.zhihu.com/collection/782323705', silent=True, mine=True)
page = MyUtils.Chrome(Aurl, silent=True, mine=True)
# page = MyUtils.Chrome(Aurl, silent=False, mine=True)
# MyUtils.skip([page,By.XPATH,'/html/body/div[1]/div/div[4]/div[1]/div[1]/a'])
time.sleep(2)

while True:
    # 获取标题，转到回答页面
    # 标题，产生新窗口
    answerurl = page.element(['/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/h2/div/a',
                              '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/span/div',
                              '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/h2/span/a',
                              '//*[@id="root"]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/span/div'])
    title = answerurl.text
    # answerurl = answerurl.get_attribute('href')
    # page.get(answerurl)
    page.click(answerurl)
    if len(page.windows())==2:
        page.switchto(-1)
    time.sleep(2)

    # 获取变量
    # 回答文本+回答元数据
    Answer = page.element(['/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]',
                           '/html/body/div[1]/div/main/div/article',
                           '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/span[1]/div',
                           '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/button[1]',
                           ])
    te = Answer.text
    if len(te) < 50:
        MyUtils.Exit(te)
    title = MyUtils.standarlizedFileName(title + te[:80])
    # StarredList=MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div'])

    # 保存文本
    if not os.path.exists(f'./知乎/plaintext/{title}.txt'):
        MyUtils.txt(f'./知乎/plaintext/{title}').add(te)

    # 截屏
    page.set_window_size(800, 2000 + Answer.size['height'])
    MyUtils.scrshot([page.element(['/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div',
                                   '/html/body/div[1]/div/main/div/article',
                                   '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]']), (f'./知乎/{title}/{title}.png')])
    time.sleep(2)

    # 回答里的图片保存
    piccount = 0
    pics = page.elements(['/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/span[1]/div/span/figure/div/img',
                          '/html/body/div[1]/div/main/div/article/div[1]/div/div/figure/div/img'])
    for pic in pics:
        url = pic.get_attribute('data-actualsrc')
        piccount += 1
        picpath = f'./知乎/{title}/{piccount}.png'
        try:
            if MyUtils.isfile(picpath):
                continue
            if False == MyUtils.pagedownload(url, picpath, t=5):
                MyUtils.Exit(-1)
        except Exception as e:
            page.look()
            MyUtils.Exit(e)

    # 取消收藏
    page.get(Aurl)
    e = page.element(['/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/button[2]',
                      '/html/body/div[1]/div/main/div/article/div[4]/div/div/button[3]'])
    if not e.text == '取消收藏':
        e = page.element('/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/button[1]')
    if not e.text == '取消收藏':
        page.look()
        MyUtils.Exit('取消收藏失败')
    page.click(e)
    time.sleep(2)

    MyUtils.log(f'已保存回答：{title}')

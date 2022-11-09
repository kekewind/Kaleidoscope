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
    # 获取标题
    answerurl = page.element(['//*[@id="root"]//main//*[@class="ContentItem-title"]',# 回答的标题
                              ])
    title = answerurl.text
    # 点击标题产生新窗口
    page.click(answerurl)
    if len(page.windows())==2:
        page.switchto(-1)
    time.sleep(2)
    # 新窗口
    Answer = page.element(['//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[@class="ContentItem AnswerItem"]',
                           '/html/body/div[1]/div/main/div/article', # 文章，全屏
                           '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/span[1]/div',
                           '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/button[1]',
                           ])
    te = Answer.text
    if len(te) < 50:
        MyUtils.Exit(te)
    title = MyUtils.standarlizedFileName(title + te[:80])

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
    pics = page.elements(['//*[@id="root"]//main//div[@class="RichContent-inner"]//figure//img'
                          ])
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
    page.driver.close()
    page.switchto(0)
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

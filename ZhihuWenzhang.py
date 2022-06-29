import MyUtils
from selenium.webdriver.common.by import By


# 打开页面
# 专栏
page=MyUtils.MyChrome()
page.get('https://zhuanlan.zhihu.com/p/25557820')
title=MyUtils.MyElement([page,By.XPATH,'/html/head/title']).get_attribute('text')
title=title[0:len(title)-5]
inc=0
for pic in MyUtils.MyElements([page,By.XPATH,'/html/body/div[1]/div/main/div/article/div[1]/div/div/figure/img']):
    inc+=1
    MyUtils.MyRequestDownload(f'./zhihu/zhuanlan/{title}/{inc}.jpg','wb',pic.get_attribute('data-original'))
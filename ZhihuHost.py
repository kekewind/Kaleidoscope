import time

import MyUtils
import requests
from selenium.webdriver.common.by import By

for HostUrl in MyUtils.file('r', './zhihu/AllUsers.txt'):
    page=MyUtils.chrome()
    page.get(HostUrl)
    MyUtils.skip([page, By.XPATH, '/html/body/div[4]/div/div/div/div[2]/button'])
    MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[1]/ul/li[3]']).click()
    for VideoUrl in MyUtils.Elements([page, By.XPATH, '//video[starts-with(@src,"https://")']):
        print(VideoUrl)
import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


# @retry(retry_on_exception=MyUtils.retry)
@MyUtils.consume
# 展开回答
def spanAnswer(l):
    page = l[0]
    # 展开
    # MyUtils.MyClick([page,By.XPATH,'/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/button'])
    MyUtils.clickelement([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/span/div/button'])
    time.sleep(2)


def answerpicture(l):
    page = l[0]
    eles = MyUtils.elements([page, By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/span/img'])
    #     获取url
    url = []
    for ele in eles:
        url.append(ele.get_attribute('data-original'))


def main():
    pass


if __name__ == '__main__':
    main()

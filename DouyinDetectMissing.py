import DouyinUtils
import MyUtils
import time
import multiprocessing
import MDouyin

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun(*a):
    (page,) = a
    missing = DouyinUtils.missing
    while missing.loopcount < missing.length():
        din = missing.get()[0]
        (num, author, title) = (MyUtils.key(din), MyUtils.value(din)['author'], MyUtils.value(din)['title'])
        for url in [f'https://douyin.com/video/{num}', f'https://douyin.com/note/{num}']:
            # 打开页面
            page.get(url)
            time.sleep(1)
            page.skip('web-login-scan-code')


def main():
    page = MyUtils.Chrome()
    fun([page])


if __name__ == '__main__':
    main()

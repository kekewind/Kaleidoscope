import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun():
    ()


def main():
    fun()


if __name__ == '__main__':
    while True:
        t=MyUtils.Time()
        if t.t.minute in[0,10,20,30,40,50]:
            MyUtils.WARN('神戒已经崩坏。')
            time.sleep(60*8)
        time.sleep(30)
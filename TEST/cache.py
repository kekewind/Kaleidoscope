import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun():
    f = MyUtils.cache(MyUtils.desktoppath('0'))
    print(f.get())


def main():
    fun()


if __name__ == '__main__':
    main()

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
    MyUtils.look(MyUtils.desktoppath('84864.txt'))

if __name__ == '__main__':
    main()

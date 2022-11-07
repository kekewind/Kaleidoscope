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
    main()
    print(MyUtils.strtotime('2022-11-06 21:52:39.267631').t.minute)
    print(MyUtils.Now().counttime(MyUtils.strtotime('2022-11-06 21:52:39.267631')))
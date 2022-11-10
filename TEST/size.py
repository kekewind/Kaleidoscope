import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun():
    size=('G:/bili/enolla_1678535/哀E静❤限定游戏❤你好二次元big胆_BV1SN4y1K7Gu')
    # size='./1.txt'
    print(MyUtils.size(size))


def main():
    fun()


if __name__ == '__main__':
    main()

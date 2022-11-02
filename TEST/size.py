import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun():
    size = (MyUtils.size('F:/bili/cache/24前羽在一线城市月薪1k2能养活自己吗-白金Saki-BV1vR4y1M78b-wcjlsHCsk7Z5wVU2/24前羽在一线城市月薪1k2能养活自己吗-白金Saki-BV1vR4y1M78b-wcjlsHCsk7Z5wVU2-video.m4s'))
    print(size / 1024)


def main():
    fun()


if __name__ == '__main__':
    main()

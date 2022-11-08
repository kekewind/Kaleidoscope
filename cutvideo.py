import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun():
    MyUtils.cutvideo(f'C:/Users/{MyUtils.user}/Pictures/WallPaper/dynamic/WP2.mp4', MyUtils.desktoppath('11.mp4'), '00:00:00', '00:03:20')


def main():
    fun()


if __name__ == '__main__':
    main()

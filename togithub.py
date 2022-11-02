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
    path = 'D:/Kaleidoscope'
    path1 = MyUtils.standarlizedPath(r'D:\Kaleidoscope\repacktogithub\Kaleidoscope')
    lis1 = MyUtils.listdir(path)
    lis2 = MyUtils.listfile(path)
    MyUtils.deletedirandfile([path1])
    MyUtils.createpath(path1)
    for i in lis1:
        if i == 'D:/Kaleidoscope/repacktogithub':
            continue
        MyUtils.copydir(i, f'{path1}/{MyUtils.tail(i, "/")}')
    for i in lis2:
        MyUtils.copyfile(i, f'{path1}/{MyUtils.tail(i, "/")}')


if __name__ == '__main__':
    main()

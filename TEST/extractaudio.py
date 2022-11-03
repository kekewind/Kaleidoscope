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
    s1="D:/VID_20221101_000916.mp4"
    s2="D:/VID_20221031_234129.mp4"
    MyUtils.extractaudio(s1,'D:/s1.m4a')

if __name__ == '__main__':
    main()

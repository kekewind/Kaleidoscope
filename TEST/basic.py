import concurrent.futures
import os
import sys

import requests
import time
from collections.abc import Iterable

import cv2
import pywin32
import MyUtils


def main(start, *a, **b):
    path = './知乎'
    print(MyUtils.accesstime(path).s())


if __name__ == "__main__":
    lis1 = MyUtils.listfile('D:/Kaleidoscope')
    lis2 = MyUtils.listdir('D:/Kaleidoscope')
    for i in lis1:
        MyUtils.copyfile(i, f'D:/Kaleidoscope/repacktogithub/Kaleidoscope/{MyUtils.gettail(i, "/")}')

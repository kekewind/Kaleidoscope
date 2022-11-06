import concurrent.futures
import os
import sys

import requests
import time
from collections.abc import Iterable

import cv2
import win32api
import win32con

import MyUtils


def main(start, *a, **b):
    path = './知乎'
    print(MyUtils.accesstime(path).s())


if __name__ == "__main__":
    win32api.MessageBox(None,'SAMPLE','title?',win32con.MB_OK)

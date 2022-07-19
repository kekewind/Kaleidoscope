import _thread
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import prompt_toolkit.clipboard.pyperclip
import prompt_toolkit.clipboard.pyperclip
import pyautogui
import pyperclip
import requests
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import Levenshtein
from PIL import Image
import MyUtils

def HostPieces(l):
    # 传入页面，返回页面上的所有pieces
    page=l[0]
    return MyUtils.MyElements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/video/")]'])

def HostElement(l):
    # 传入主页的作品元素，返回元素的Url，链接
    VideolElement=l[0]
    elementurl = VideolElement.get_attribute('href')
    VideoNum = elementurl[elementurl.rfind('/') + 1:len(elementurl)]
    return (elementurl,VideoNum)

def IsPic(l):
    # 传入元素，返回是否是图文（真）还是视频
    element=l[0]
    t=MyUtils.MyElement([element, By.XPATH, './div/div[3]/div/div'], depth=9, show=MyUtils.debug)
    # 先收集普通的图文标签
    if t==None:
        t=MyUtils.MyElement([element, By.XPATH, './div/div[3]/div/span'], depth=10, show=MyUtils.debug)
    #     收集置顶标签
    if t==None:
    #     什么标签也没有
        return False
    t=t.text
    MyUtils.delog(f'检测到元件标签为 {t}')
    if t=='图文':
        return True
    else:
        if t=='置顶'or t=='挑战榜'or t=='热榜':
            t=MyUtils.MyElement([element, By.XPATH, './div/div[3]/div[2]'], depth=8, show=MyUtils.debug)
        if t==None:
            return False
        else:
            return True


def Title(l):
    # 传入网页，返回作品标题
    page=l[0]
    title = MyUtils.MyTitle([page])
    if title:
        return title.strip(' - 抖音')
    else:
        print(f'[DouyinUtils][Title] 获取title 失败。you may try {page.current_url}')

MyUtils.log('DouyinUtils loaded.')
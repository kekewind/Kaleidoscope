import sys

import selenium.webdriver.remote.webelement
from selenium.webdriver.common.by import By

import MyUtils
import json


def HostPieces(l):
    # 传入页面，返回页面上的所有pieces
    page=l[0]
    ret=MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/video/")]'])
    MyUtils.delog(f'准备操作的作品列表长度：{len(ret)}')
    return ret

def HostElement(l):
    # 传入主页的作品元素，返回元素的Url，链接
    VideolElement=l[0]
    elementurl = VideolElement.get_attribute('href')
    if elementurl.find('?')>0:
        VideoNum = elementurl[elementurl.rfind('/') + 1:elementurl.find('?')]
    else:
        VideoNum = elementurl[elementurl.rfind('/') + 1:]
    return (elementurl,VideoNum)

def IsPic(l):
    # 传入元素，返回是否是图文（真）还是视频
    # 如果没有消除二维码页面，会冻结检测。
    page=l[0]
    element=l[1]
    elements=MyUtils.Elements([element, By.XPATH, './div/div[3]/div'], depth=9)
    # 第一、二、三个标签
    # 思路是找到一个图文标签即可
    for el in elements:
        if not None==MyUtils.Element([el,By.XPATH,'./div'], depth=9):
            # svg找不到
            return True
    return False

def Title(l):
    # 传入网页，返回作品标题
    page=l[0]
    title = MyUtils.MyTitle([page])
    if title:
        return title.strip(' - 抖音')
    else:
        print(f'[DouyinUtils][Title] 获取title 失败。you may try {page.current_url}')

def PieceInfo():
    disk=''
    url=''
    author=''
    UserUID=''
    num=0
    type=''
    title=''
    return {'dick':disk,'url':url,'author':author,'num':num,'type':type,'UserUID':UserUID,'title':title}

def simplinfo(num,author,title):
    return json.dumps({str(num):{'disk':MyUtils.hashdisk,'author':author,'title':title}},ensure_ascii=False)
    # return json.dumps({str(num):{'disk':MyUtils.hashdisk,'author':author,'title':title}},ensure_ascii=True)
#   上面这个把中文转码

MyUtils.tip('DouyinUtils loaded.')
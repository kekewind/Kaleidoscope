import sys

import selenium.webdriver.remote.webelement
from selenium.webdriver.common.by import By

import MyUtils
import json
import time


def HostPieces(l):
    # 传入页面，返回页面上的所有pieces
    page=l[0]
    ret=[]
    l1=MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"/video/")]'],depth=9)
    l2=MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/note/")]'],depth=9)
    l3=MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/video/")]'],depth=9)
    ret=MyUtils.extend(ret,l1)
    ret=MyUtils.extend(ret,l2)
    ret=MyUtils.extend(ret,l3)

    if ret==[]:
        MyUtils.warn('获取视频元素列表错误。')
        sys.exit(0)
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
    author=''
    num=0
    type=''
    title=''
    return {'dick':disk,'url':url,'author':author,'num':num,'type':type,'UserUID':UserUID,'title':title}

def simplinfo(num,author,title):
    return json.dumps({str(num):{'disk':MyUtils.diskname, 'author':author, 'title':title}}, ensure_ascii=False)
    # return json.dumps({str(num):{'disk':MyUtils.hashcode,'author':author,'title':title}},ensure_ascii=True)
#   上面这个把中文转码

def getPiecesNum(l):
    page=l[0]
    MyUtils.setscrolltop([page, 0])
    time.sleep(0.2)
    l1 = MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span'],depth=9)
    l2 = MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/span[2]'],depth=9)
    ret=0
    if not l1==None:
        ret= int(l1.text)
    elif not l2==None:
        ret= int(l2.text)
    MyUtils.delog(f'作品数量：{ret}')
    return ret


MyUtils.tip('DouyinUtils loaded.')


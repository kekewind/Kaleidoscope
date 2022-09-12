import json
import os
import sys
import time

from selenium.webdriver.common.by import By

import MyUtils

allusers = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/AllUsers.txt')
allpieces = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/AllPieces.txt')

readytodownload = MyUtils.cache('D:/Kaleidoscope/抖音/ReadytoDownload.txt')
exceptuser = MyUtils.txt('D:/Kaleidoscope/抖音/FailedUsers.txt')
failed = MyUtils.Json('D:/Kaleidoscope/抖音/FailedPieces.txt')
missing=MyUtils.rjson('D:/Kaleidoscope/抖音/Missing.txt')

diskusers=[]
for i in MyUtils.listdir('./抖音/'):
    diskusers.append(MyUtils.filename(i))

# 页面-所有pieces ele
def HostPieces(l):
    page = l[0]
    ret = []
    time.sleep(5)
    l2 = MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/note/")]'], depth=10, silent=True)
    l3 = MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/video/")]'], depth=10, silent=True)
    l1 = MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"/video/")]'], depth=10, silent=True)
    ret = MyUtils.extend(ret, l1)
    ret = MyUtils.extend(ret, l2)
    ret = MyUtils.extend(ret, l3)

    if ret == []:
        MyUtils.warn(f'获取视频元素列表错误。{l1, l2, l3}')
        sys.exit(-1)
    MyUtils.delog(f'准备操作的作品列表长度：{len(ret)}')
    return ret


# piece ele-url, num
def piecetourlnum(l):
    VideolElement = l[0]
    elementurl = VideolElement.get_attribute('href')
    if elementurl.find('?') > 0:
        VideoNum = elementurl[elementurl.rfind('/') + 1:elementurl.find('?')]
    else:
        VideoNum = elementurl[elementurl.rfind('/') + 1:]
    return (elementurl, VideoNum)


def addauthor(useruid, author, users=allusers):
    User = None
    for i in users.l:
        if not useruid == list(MyUtils.jsontodict(i).keys())[0]:
            continue
        else:
            User = i
    if User == None:
        users.add({useruid: [author]})
        MyUtils.delog(f'添加了新用户在{users.path}中')
        return
    authors = MyUtils.jsontodict(User)[useruid]
    if not author in authors:
        users.add({useruid: MyUtils.extend(authors, [author])})
        MyUtils.delog(f'添加了用户名称在{users.path}中')


def IsPic(l):
    # 传入元素，返回是否是图文（真）还是视频
    # 如果没有消除二维码页面，会冻结
    stole = MyUtils.nowstr()
    element = l[0]
    elements = MyUtils.Elements([element, By.XPATH, './div/div[3]/div'], depth=9, silent=True)
    # 第一、二、三个标签
    # 思路是找到一个图文标签即可
    for el in elements:
        if not None == MyUtils.Element([el, By.XPATH, './div'], depth=9, silent=True):
            # svg找不到
            return True
    return False


def Title(l):
    # 传入网页，返回作品标题
    page = l[0]
    title = MyUtils.MyTitle([page])
    if title:
        return title.strip(' - 抖音')
    else:
        print(f'[DouyinUtils][Title] 获取title 失败。you may try {page.current_url}')


# def PieceInfo():
#     disk=''
#     author=''
#     num=0
#     type=''
#     title=''
#     return {'dick':disk,'url':url,'author':author,'num':num,'type':type,'useruid':useruid,'title':title}

def simplinfo(num, author, title):
    return json.dumps({str(num): {'disk': MyUtils.diskname, 'author': author, 'title': title}}, ensure_ascii=False)
    # return json.dumps({str(num):{'disk':MyUtils.hashcode,'author':author,'title':title}},ensure_ascii=True)


#   上面这个把中文转码

# 获取作品数量
def HostPiecesNum(l):
    page = l[0]
    MyUtils.setscrolltop([page, 0])
    time.sleep(0.2)
    l1 = MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span'], depth=9, silent=True)
    l2 = MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/span[2]'], depth=9, silent=True)
    ret = 0
    if not l1 == None:
        ret = int(l1.text)
    elif not l2 == None:
        ret = int(l2.text)
    else:
        MyUtils.warn(f'作品数量获取失败.。{l1, l2}')
    MyUtils.delog(f'作品数量：{ret}')
    return ret


def HostPiecesLike(l):
    page = l[0]
    l1 = MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[2]/span'], depth=9, silent=True)
    l2 = MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/span[2]'], depth=9, silent=True)
    LikeElement = MyUtils.extend(l1, l2)[0]
    LikeNum = LikeElement.text
    LikeElement.click()
    return LikeNum


def skiprecorded(VideoNum):
    if (VideoNum in allpieces.d.keys()):
        MyUtils.log(f'作品{VideoNum}在记录中，跳过')
        return True
    return False


def skipdownloaded(flag, record, VideoNum, title, author):
    path = './抖音/' + author
    if os.path.exists(f'{path}/{title}.mp4') and not flag:
        record.add(simplinfo(VideoNum, author, title))
        MyUtils.log(f' {path}/{title}.mp4已存在磁盘中，补全记录')
        return True
    if flag and os.path.exists(f'{path}/{title}/{len(VideoNum) - 1}.png'):
        record.add(simplinfo(VideoNum, author, title))
        MyUtils.log(f' {path}/{title}共{len(VideoNum)}张图片已存在磁盘中，补全记录')
        return True
    return False


def dislike(l):
    page = l[0]
    l1 = MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div[1]'], depth=9)
    l2 = MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[2]/div/div[1]/div[1]'], depth=9)
    MyUtils.click([page, MyUtils.extend(l1, l2)[0]])
    time.sleep(3)
    # ???貌似要等很久？


# 加入准备下载
def load(flag, page, VideoNum, author, title, readytoDownload=readytodownload):
    VideoUrl = []
    if not flag:
        # region
        element = MyUtils.Element(depth=5, l=[page, By.XPATH, '//xg-video-container/video/source[1]'])
        if element == None:
            MyUtils.warn(f'获取作品下载地址失败。元素未获取到。')
            page.quit()
            raise(MyUtils.MyError)
        VideoUrl = [element.get_attribute('src')]
        #     endregion
    else:
        # region
        elements = MyUtils.Elements(depth=7, l=[page, By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[1]/div/div[2]/div/img'])
        for e in elements:
            https = e.get_attribute('src')
            VideoUrl.append(https)
        #     endregion
    readytoDownload.add({"list": [VideoNum, author, title, VideoUrl, flag]})
    MyUtils.delog([(VideoNum, author, title, VideoUrl, flag), '准备下载列表readytoDownload  added.'])


MyUtils.tip('DouyinUtils loaded.')

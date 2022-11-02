import MyUtils
import time
import sys
import json
import os

from retrying import retry
from selenium.webdriver.common.by import By

allusers = MyUtils.rjson('D:/Kaleidoscope/tiktok/moena315.txt')
allpieces = MyUtils.RefreshJson('D:/Kaleidoscope/tiktok/AllPieces.txt')

readytodownload = MyUtils.cache('D:/Kaleidoscope/tiktok/ReadytoDownload.txt')
exceptuser = MyUtils.txt('D:/Kaleidoscope/tiktok/FailedUsers.txt')
failed = MyUtils.Json('D:/Kaleidoscope/tiktok/FailedPieces.txt')
missing = MyUtils.rjson('D:/Kaleidoscope/tiktok/Missing.txt')


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
    title = MyUtils.title([page])
    if title:
        return title.strip(' - 抖音')
    else:
        print(f'[DouyinUtils][Title] 获取title 失败。you may try {page.current_url}')


# 更新User列表
def addauthor(useruid, author, users=allusers):
    User = None
    for i in users.l:
        if not useruid == list(MyUtils.jsontodict(i).keys())[0]:
            continue
        else:
            User = i
            break
    if User == None:
        users.add({useruid: [author]})
        MyUtils.delog(f'添加了新用户在{users.path}中')
        return
    authors = MyUtils.jsontodict(User)[useruid]
    if not author in authors:
        users.add({useruid: MyUtils.extend(authors, [author])})
        MyUtils.delog(f'添加了用户名称在{users.path}中')


# 页面-所有pieces ele
def HostPieces(l):
    page = l[0]
    ret = []
    time.sleep(5)
    l2 = MyUtils.Elements([page, By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/a'], depth=10, silent=True)
    # l3 = MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/video/")]'], depth=10, silent=True)
    # l1 = MyUtils.Elements([page, By.XPATH, '//a[starts-with(@href,"/video/")]'], depth=10, silent=True)
    # ret = MyUtils.extend(ret, l1)
    ret = MyUtils.extend(ret, l2)
    # ret = MyUtils.extend(ret, l3)

    if ret == []:
        MyUtils.warn(f'获取视频元素列表错误。{l2}')
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


def skipdownloaded(flag, record, VideoNum, title, author):
    path = './tiktok/' + author
    if (os.path.exists(f'{path}/{title}.mp4') and not flag) or (os.path.exists(f'{path}/{VideoNum}_{title}.mp4') and not flag):
        record.add(simplinfo(VideoNum, author, title))
        MyUtils.log(f' {path}/{title}.mp4已存在磁盘中，补全记录')
        return True
    if (flag and os.path.exists(f'{path}/{title}/{len(VideoNum) - 1}.png')) or (flag and os.path.exists(f'{path}/{VideoNum}_{title}/{len(VideoNum) - 1}.png')):
        record.add(simplinfo(VideoNum, author, title))
        MyUtils.log(f' {path}/{title}共{len(VideoNum)}张图片已存在磁盘中，补全记录')
        return True
    return False


# 加入准备下载
def load(flag, page, VideoNum, author, title, readytoDownload=readytodownload):
    VideoUrl = []
    if not flag:
        # region
        element = MyUtils.Element(depth=5, l=[page, By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div/div/video'])
        if element == None:
            MyUtils.warn(f'获取作品下载地址失败。元素未获取到。')
            page.quit()
            raise (MyUtils.MyError)
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


def skiprecorded(VideoNum):
    if (VideoNum in allpieces.d.keys()):
        MyUtils.log(f'作品{VideoNum}在记录中，跳过')
        return True
    return False


def simplinfo(num, author, title):
    return json.dumps({str(num): {'disk': MyUtils.diskname, 'author': author, 'title': title}}, ensure_ascii=False)
    # return json.dumps({str(num):{'disk':MyUtils.hashcode,'author':author,'title':title}},ensure_ascii=True)


def main():
    pass


if __name__ == '__main__':
    main()

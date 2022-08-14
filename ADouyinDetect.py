import asyncio
import os.path
import sys
import time
import multiprocessing

from selenium.webdriver.common.by import By

import DouyinUtils
import Maintainace
import MyUtils

# 变量
UserList=MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
record=MyUtils.RefreshJson('D:/Kaleidoscope/抖音/Distripute.txt')
readytoDownload=MyUtils.cache('D:/Kaleidoscope/抖音/ReadytoDownload.txt')
Host = MyUtils.edge()
page=MyUtils.edge()
UserUID='nothing'

def detect():
    # 探测
    stole = MyUtils.now()
    # 获取参数
    # region
    flag = DouyinUtils.IsPic([Host, VideoElement])
    # endregion

    # 作品网页
    page.get(elementurl)
    MyUtils.delog(f' trying to get {elementurl} ...')

    # 如果是图片
    if flag:
        page.get(f'https://www.douyin.com/note/{VideoNum}')
    # 如果是视频
    else:
        page.get(f'https://www.douyin.com/video/{VideoNum}')
    # region
    time.sleep(0.5)
    # endregion

    # 获取参数-标题
    # region
    title = DouyinUtils.Title([page])
    # MyUtils.delog(f' title={title}')
    # endregion

    # 如果当前操作磁盘里有，增加记录
    # region
    MyUtils.delog((f'{os.path.abspath(path)}/{title}.mp4', flag))
    if os.path.exists(f'{path}/{title}.mp4') and not flag:
        record.add(DouyinUtils.simplinfo(VideoNum, author, title))
        MyUtils.log(f' {path}/{title}.mp4已存在磁盘中，补全记录')
        MyUtils.log(f'{MyUtils.counttime(stole)}s')
        return
    if flag and os.path.exists(f'{path}/{title}/{len(VideoNum) - 1}.png'):
        record.add(DouyinUtils.simplinfo(VideoNum, author, title))
        MyUtils.log(f' {path}/{title}共{len(VideoNum)}张图片已存在磁盘中，补全记录')
        MyUtils.log(f'{MyUtils.counttime(stole)}s')
        return
    # endregion

    # 获取下载地址
    time.sleep(1)
    VideoUrl = []
    if not flag:
        # region
        element = MyUtils.Element(depth=7, l=[page, By.XPATH, '//xg-video-container/video/source[1]'])
        if element == None:
            MyUtils.warn(f'获取作品下载地址失败。元素未获取到。')
        VideoUrl = [element.get_attribute('src')]
        #     endregion
    else:
        # region
        elements = MyUtils.Elements(show=None, l=[page, By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[1]/div/div[2]/div/img'])
        for e in elements:
            https = e.get_attribute('src')
            VideoUrl.append(https)
        #     endregion
    readytoDownload.add({"list":[VideoNum,author,title,VideoUrl,flag]})
    MyUtils.delog('readytoDownload added.')
    MyUtils.log(f'{MyUtils.counttime(stole)}s')

# 开始用户循环
while UserUID:
    UserUID=UserList.get()

    # 清除UserUID的https://www.douyin.com/user/前缀
    # region
    if UserUID.find('www.douyin.com') > 0:
        UserList.delete(UserUID)
        UserUID.replace('https://www.douyin.com/user/', '')
        UserList.add(UserUID)
    # endregion

    # 用户主页
    # region
    HostUrl='https://www.douyin.com/user/' + UserUID.replace('https://www.douyin.com/user/', '')
    Host.get(HostUrl)
    # 为什么这句会有两次import输出？？？
    # endregion
    # 获取变量
    # region
    MyUtils.skip([Host, By.ID, "captcha-verify-image"])
    MyUtils.skip([Host, By.ID, "login-pannel"])
    author = MyUtils.Element([Host, By.XPATH, '/html/head/title']).get_attribute('text')
    author = author[0:author.rfind('的主页')]
    path = '../抖音/' + author
    MyUtils.log(f'  ------转到{author}的主页-----')
    MyUtils.delog(HostUrl)
    douyinSum=0
    try:
        MyUtils.setscrolltop([Host, 0])
        time.sleep(0.2)
        PiecesNum = int(MyUtils.Element([Host, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span']).text)
        MyUtils.delog(f'作品数量：{PiecesNum}')
    except:
        UserList.Rollback()
        MyUtils.warn(f'https://www.douyin.com/user/{UserUID}获取作品数目异常。')
        continue
    # pool2=multiprocessing.Pool(maxworker2)
    # endregion
    # 滑动滑块
    # region
    MyUtils.scroll([Host])
    # endregion
    # endregion
    # 获取变量
    # region
    # endregion

    # 作品列表循环
    for VideoElement in DouyinUtils.HostPieces([Host]):
        # 获取变量
        # region
        (elementurl, VideoNum) = DouyinUtils.HostElement([VideoElement])
        # endregion
        # 跳过已下载
        # region
        if (VideoNum in record.d.keys()):
            MyUtils.log(f'{author}的作品{VideoNum}在记录中，跳过')
            continue
        # endregion
        detect()
        douyinSum+=1
        if douyinSum>=70:
            break
    record.save()

# 结束
# region
record.save()
#     endregion


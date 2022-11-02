import os.path
import sys
import time
import multiprocessing

from selenium.webdriver.common.by import By

import DouyinUtils
import Maintainace
import MyUtils

MyUtils.Debug()


# 结束
def end():
    LocalUserSpectrum.save()
    Distripute.save()
    MyUtils.dicttofile(Distripute, './抖音/AllPieces.txt')
    MyUtils.log(f'已下载{Distripute.length()} 用户数量{LocalUserSpectrum.length()} 失败数{Failed.length()}')
    DouyinHost.quit()
    sys.exit()


# 下载
def download():
    # MyUtils.delog('a')
    global DouyinSum
    while len(ReadyToDownload):
        stole = MyUtils.strtotime()
        # 获取参数
        # region
        (VideoNum, (HostID, title, VideoUrl)) = ReadyToDownload.popitem()
        path = '../抖音/' + HostID
        MyUtils.delog(f'VideoNum={VideoNum} HostID={HostID} title={title} VideoUrl={VideoUrl}')
        # endregion
        # 判断是否图文
        if not len(VideoUrl) > 1:
            # 视频
            # region
            MyUtils.delog(f'开始下载，url={VideoUrl[0]}')
            t = MyUtils.pagedownload(url=VideoUrl[0], path=f'{path}/{title}.mp4')
            #     endregion
        else:
            # 图片
            # region
            t = True
            i = 0
            for url in VideoUrl:
                i += 1
                MyUtils.delog(f'开始下载，url={url}')
                t = MyUtils.pagedownload(url=url, path=f'{path}/{title}/{i}.png') and t
            #     endregion

        # 是否下载成功
        if t:
            # region
            Distripute.add(VideoNum)
            MyUtils.log(f'下载成功，{VideoNum}记录补全.\n{DouyinSum}]{HostID}  :作品编号：{VideoNum}     作品标题：{title}\n{VideoUrl}')
            DouyinSum += 1
            # endregion
        else:
            # region
            Failed.add(title + '.mp4.crdownload')
            MyUtils.warn(f'下载失败，{VideoNum}记录补全到 Failed.\n{DouyinSum}]{HostID}  :作品编号：{VideoNum}     作品标题：{title}\n{VideoUrl}')
            # endregion

        MyUtils.log(f'cost{MyUtils.strtotime() - stole}')


# 探测
def detect(path, author, VideoNum, l):
    MyUtils.delog('a')
    stole = MyUtils.strtotime()
    # 获取参数
    # region
    index = isPageUsing.index(0)
    MyUtils.delog(index)
    isPageUsing[index] = 1
    page = pages[index]
    (flag,) = l
    # endregion
    MyUtils.delog(f' trying to get {f"https://www.douyin.com/video/{VideoNum}"} ...')

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
    if os.path.exists(f'{path}/{title}.mp4') and not flag:
        Distripute.add(DouyinUtils.simplinfo(VideoNum, author, title))
        MyUtils.log(f' Detect{index + 1}: {path}/{title}.mp4已存在磁盘中，补全记录')
        isPageUsing[index] = 0
        MyUtils.log(f'Detect{index + 1} {MyUtils.counttime(stole)}s')
        return
    if flag and os.path.exists(f'{path}/{title}/{len(VideoNum) - 1}.png'):
        Distripute.add(DouyinUtils.simplinfo(VideoNum, author, title))
        MyUtils.log(f' Detect{index + 1}: {path}/{title}共{len(VideoNum)}张图片已存在磁盘中，补全记录')
        isPageUsing[index] = 0
        MyUtils.log(f'Detect{index + 1} done. cost {MyUtils.counttime(stole)}s')
        return
    # endregion

    # 获取下载地址
    VideoUrl = []
    if not flag:
        # region
        VideoUrl = [MyUtils. \
                        Element(show=None, l=[page, By.XPATH,
                                              '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-video-container/video/source[1]']) \
                        .get_attribute('src')]
        #     endregion
    else:
        # region
        elements = MyUtils.Elements(show=None, l=[page, By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[1]/div/div[2]/div/img'])
        for e in elements:
            https = e.get_attribute('src')
            VideoUrl.append(https)
        #     endregion
    ReadyToDownload.update({VideoNum: (author, title, VideoUrl)})

    # MyUtils.log(({VideoNum:(author,title,VideoUrl)}))
    # MyUtils.log(f' Detect{index+1}:探测到未下载。准备下载增加，{len(ReadyToDownload)}')

    # 结束
    # region
    isPageUsing[index] = 0
    MyUtils.log(f'Detect{index + 1} {MyUtils.counttime(stole)}s')
    return
    #     endregion


if __name__ == '__main__':

    # 初始化参数
    # region
    Maintainace.SeleniumSpace()
    Failed = MyUtils.RefreshTXT('抖音/FailedPieces.txt')
    LocalUserSpectrum = MyUtils.RefreshTXT('抖音/AllUsers.txt')
    # Distripute = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/VideoSpectrum.txt')
    Distripute = MyUtils.RefreshJson('抖音/AllPieces.txt')
    MyUtils.log(f'LocalVideo:{Distripute.length()} LocalUser:{LocalUserSpectrum.length()} Failed:{Failed.length()}')
    ReadyToDownload = {}
    DouyinSum = 1
    maxworkers = 1
    maxworkers1 = 1
    DouyinHost = MyUtils.edge()
    isPageUsing = [0 for i in range(maxworkers)]
    UserUID = LocalUserSpectrum.l[0]
    pages = [MyUtils.edge() for i in range(maxworkers)]
    # endregion

    # 对用户循环
    while UserUID != None:
        # 线程池等变量初始化
        # region
        pool1 = multiprocessing.Pool(maxworkers)
        # pool2=multiprocessing.Pool(maxworkers1)
        UserUID = LocalUserSpectrum.get()
        # useruid='MS4wLjABAAAAiFr5ORhuw0jQALgakjhQ-QKuYK6LEuifcdwLGxHORzA'
        # endregion

        # 清除UserUID的https://www.douyin.com/user/前缀
        # region
        if UserUID.find('www.douyin.com') > 0:
            LocalUserSpectrum.delete(UserUID)
            UserUID.replace('https://www.douyin.com/user/', '')
            LocalUserSpectrum.add(UserUID)
        # endregion

        # 打开用户主页操作
        # region
        # 转到网页
        # region
        DouyinHost.get('https://www.douyin.com/user/' + UserUID.replace('https://www.douyin.com/user/', ''))
        # 为什么这句会有两次import输出？？？
        # endregion
        # 验证码跳过
        # region
        MyUtils.skip([DouyinHost, By.ID, "captcha-verify-image"], True)
        # MyUtils.MySkip([DouyinHost, By.ID, "login-pannel"])
        # endregion
        # 获取变量
        # region
        author = MyUtils.Element([DouyinHost, By.XPATH, '/html/head/title']).get_attribute('text')
        author = author[0:author.rfind('的主页')]
        path = '../抖音/' + author
        MyUtils.log(f'  ------已转到{author}的主页-----')
        # endregion
        # 滑动滑块
        # region
        # MyUtils.MyScroll([DouyinHost])
        # endregion
        # 获取作品数量
        # region
        try:
            MyUtils.setscrolltop([DouyinHost, 0])
            time.sleep(0.2)
            PiecesNum = int(MyUtils.Element([DouyinHost, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span']).text)
            MyUtils.delog(f'作品数量：{PiecesNum}')
        except:
            LocalUserSpectrum.Rollback()
            MyUtils.warn(f'https://www.douyin.com/user/{UserUID}获取作品数目异常。')
            continue
        # endregion
        # endregion

        # 作品列表循环
        ttt = DouyinUtils.HostPieces([DouyinHost])
        for VideoElement in ttt:
            # 获取变量
            # region
            (elementurl, VideoNum) = DouyinUtils.piecetourlnum([VideoElement])
            i = 0
            # endregion
            # 跳过已下载
            # region
            # if (VideoNum in Distripute.d.keys()):
            #     MyUtils.log(f'{author}的作品{VideoNum}在记录中，跳过')
            #     continue
            # endregion
            # 探测请求detect
            pool1.apply_async(detect, args=(path, author, VideoNum, [DouyinUtils.IsPic([VideoElement])]))
            # detect(path, author, VideoNum, [VideoElement])
        pool1.close()
        pool1.join()
        MyUtils.delog(-1)
        MyUtils.log(f'下载队列长度{len(ReadyToDownload)}')

        # 下载请求
        # for i in range(maxworkers1):
        # pool2.apply_async(download,args=())
        # download()
        # pool2.close()
        # pool2.join()

        # 收尾
        # region
        Distripute.save()
        MyUtils.log(f"用户{author}已完成  剩余User总量{LocalUserSpectrum.loopcount}/{LocalUserSpectrum.length()}]")
        #     endregion
    end()

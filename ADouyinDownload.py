import multiprocessing
import os.path
import sys
import threading
import time

from selenium.webdriver.common.by import By

import DouyinUtils
import Maintainace
import MyUtils

MyUtils.Debug()
# 下载
def download():
    stole=MyUtils.gettime()
    MyUtils.delog('a')
    global DouyinSum
    while len(ReadyToDownload):
        (VideoNum, (HostID, title, VideoUrl)) = ReadyToDownload.popitem()
        MyUtils.delog(f'VideoNum={VideoNum} HostID={HostID} title={title} VideoUrl={VideoUrl}')
        if not len(VideoUrl) > 1:
            # 视频
            path = '../抖音/' + HostID
            MyUtils.delog(f'开始下载，url={VideoUrl[0]}')
            t = MyUtils.MyPageDownload(url=VideoUrl[0], path=f'{path}/{title}.mp4')
        else:
            # 图文
            path = '../抖音/' + HostID
            t = True
            i = 0
            for url in VideoUrl:
                i += 1
                MyUtils.delog(f'开始下载，url={url}')
                t = MyUtils.MyPageDownload(url=url, path=f'{path}/{title}/{i}.png')
        if t:
            LocalVideoSpectrum.add(VideoNum)
            MyUtils.log(f'{MyUtils.MyTime("hms")}\n[Download]下载成功，{VideoNum}记录补全.'+\
                        '\n'+f'{DouyinSum}]{HostID}  :', f'作品编号：{VideoNum}     作品标题：{title}\n{VideoUrl}')
            DouyinSum += 1
            MyUtils.delog(0)
        else:
            Failed.add(title + '.mp4.crdownload')
            MyUtils.log(f'下载失败，记录增加')

    MyUtils.log(f'cost{-stole+MyUtils.gettime()}')


#
def detect(path, HostID, VideoNum, l):
    stole=MyUtils.gettime()
    element = l[0]
    index = isPageUsing.index(0)
    isPageUsing[index] = 1
    page = PageRe[index]
    MyUtils.delog(f' trying to get {f"https://www.douyin.com/video/{VideoNum}"} ...')

    # 判断是图文
    flag = DouyinUtils.IsPic([element])
    # MyUtils.log(f' flag={flag} VideoNum={VideoNum}')
    if flag:
        page.get(f'https://www.douyin.com/note/{VideoNum}')
        # 删除已经存在的.mp4（以前误下载的）
    else:
        # 判断是视频
        page.get(f'https://www.douyin.com/video/{VideoNum}')
    time.sleep(0.5)

    # 获取标题
    title = DouyinUtils.Title([page])
    MyUtils.delog(f' title={title}')
    # 如果下载过
    if os.path.exists(f'{path}/{title}.mp4') and not flag:
        LocalVideoSpectrum.add(VideoNum)
        MyUtils.log(f' Robot{index + 1}: {HostID}{title}.mp4已存在磁盘中，补全记录')
        isPageUsing[index] = 0
        MyUtils.log(f'Robot{index + 1} {MyUtils.counttime(stole)}s')
        return
    if flag and os.path.exists(f'{path}/{title}/{len(VideoNum) - 1}.png'):
        LocalVideoSpectrum.add(VideoNum)
        MyUtils.log(f' Robot{index + 1}: {path}/{title}共{len(VideoNum)}张图片已存在磁盘中，补全记录')
        isPageUsing[index] = 0
        MyUtils.log(f'Robot{index + 1} done. cost {MyUtils.counttime(stole)}s')
        return


    # 获取下载地址
    VideoUrl = []
    if not flag:
        VideoUrl = [MyUtils. \
                        MyElement(silent=True, l=[page, By.XPATH,
                                                  '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-video-container/video/source[1]']) \
                        .get_attribute('src')]
    else:
        elements = MyUtils.MyElements(silent=True, l=[page, By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[1]/div/div[2]/div/img'])
        for e in elements:
            https = e.get_attribute('src')
            VideoUrl.append(https)
    ReadyToDownload.update({VideoNum: (HostID, title, VideoUrl)})
    # MyUtils.log(({VideoNum:(HostID,title,VideoUrl)}))
    # MyUtils.log(f' Robot{index+1}:探测到未下载。准备下载增加，{len(ReadyToDownload)}')
    isPageUsing[index] = 0
    MyUtils.log(f'Robot{index + 1} {MyUtils.counttime(stole)}s')
    return


def end():
    LocalUserSpectrum.save()
    LocalVideoSpectrum.save()
    MyUtils.log(f'已下载{LocalVideoSpectrum.length()} 用户数量{LocalUserSpectrum.length()} 失败数{Failed.length()}')
    DouyinHost.quit()
    sys.exit()


# 初始化
Maintainace.Space()
Failed = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/Failed.txt')
LocalUserSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
LocalVideoSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/VideoSpectrum.txt')
MyUtils.log(f'LocalVideo:{LocalVideoSpectrum.length()} LocalUser:{LocalUserSpectrum.length()} Failed:{Failed.length()}')
UserUID = 1
ReadyToDownload = {}
DouyinSum = 1
maxworkers = 2
maxworkers1 = 2
DouyinHost = MyUtils.MyEdge()
isPageUsing = [0 for i in range(maxworkers)]
UserUID = LocalUserSpectrum.l[0]
PageRe = [MyUtils.MyEdge() for i in range(maxworkers)]


while UserUID != None:
    # pool1=multiprocessing.Pool(maxworkers)
    # pool2=multiprocessing.Pool(maxworkers1)
    # UserUID = LocalUserSpectrum.get()
    UserUID='MS4wLjABAAAAiFr5ORhuw0jQALgakjhQ-QKuYK6LEuifcdwLGxHORzA'
    if UserUID.find('www.douyin.com') > 0:
        LocalUserSpectrum.delete(UserUID)
        UserUID.replace('https://www.douyin.com/user/', '')
        LocalUserSpectrum.add(UserUID)
    # 用户循环，并自动去掉UserUID的url前缀


    # 用户主页
    DouyinHost.get('https://www.douyin.com/user/' + UserUID.replace('https://www.douyin.com/user/', ''))
    MyUtils.MySkip([DouyinHost, By.ID, "captcha-verify-image"])
    # MyUtils.MySkip([DouyinHost, By.ID, "login-pannel"])
    HostID = MyUtils.MyElement([DouyinHost, By.XPATH, '/html/head/title']).get_attribute('text')
    HostID = HostID[0:HostID.rfind('的主页')]
    path = '../抖音/' + HostID
    MyUtils.log(f'  ------已转到{HostID}的主页-----')
    if not MyUtils.debug:
        MyUtils.MyScroll([DouyinHost])
    try:
        MyUtils.MySetScrollTop([DouyinHost,0])
        time.sleep(0.2)
        PiecesNum = int(MyUtils.MyElement([DouyinHost, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span']).text)
    except:
        LocalUserSpectrum.Rollback()
        MyUtils.warn(f'https://www.douyin.com/user/{UserUID}获取作品数目异常。')
        continue
    # 作品列表循环
    for VideolElement in DouyinUtils.HostPieces([DouyinHost]):
        (elementurl, VideoNum) = DouyinUtils.HostElement([VideolElement])
        i = 0
        # 如果下载过
        if (VideoNum in LocalVideoSpectrum.l) and not MyUtils.debug:
            MyUtils.log(f'{HostID}的作品{VideoNum}在记录中，跳过')
            continue


        #     同时进行请求队列减速
        # depth = 0
        # while isPageUsing == [1 for i in range(maxworkers)]:
        #     MyUtils.log(f'detect队列已满 预备下载队列长度{len(ReadyToDownload)} detect队列实时工作{e.cool} / {e.max_workers}')
        #     time.sleep(10)
        #     depth += 1
        #     if depth > 30:
        #         MyUtils.log('疑似线程已死亡，主线程开始下载并准备结束。')
        #         while len(ReadyToDownload):
        #             e1.add(Download)
        #         while e1.cool:
        #             time.sleep(10)
        #             MyUtils.log(f'等待最后的下载队列完毕。len(ReadtToDownload):{len(ReadyToDownload)}, e.cool:{e.cool}')
        #         # 结束
        #         LocalVideoSpectrum.save()
        #         MyUtils.log('LocalVideo: ', LocalVideoSpectrum.length(), ' LocalUser: ', LocalUserSpectrum.length(), f'Failed:{Failed.length()}')
        #         DouyinHost.quit()
        #         sys.exit()

        # pool1.apply_async(detect,args=(path, HostID, VideoNum, [VideolElement]))
        detect(path, HostID, VideoNum, [VideolElement])
        # pool2.apply_async(download,args=())
        download()
        MyUtils.log(f'下载队列长度{len(ReadyToDownload)}')
    # pool1.join()
    # pool1.close()

    # depth = 0
    # while e1.cool > 3 or len(ReadyToDownload):
    #     if not e1.isFulling():
    #         e1.add(Download)
    #     MyUtils.log(f'等待{HostID}下载队列完成，实时工作数：{e1.cool} / 最大容量：{e1.max_workers} / 剩余任务数：{len(ReadyToDownload)}')
    #     time.sleep(10)
    #     if e1.cool < 3:
    #         depth += 1
    #     if depth > 30:
    #         MyUtils.log('下载队列好像异常了')
    #         break
    LocalVideoSpectrum.save()
    MyUtils.log(f"用户{HostID}已完成  剩余User总量{LocalUserSpectrum.loopcount}/{LocalUserSpectrum.length()}]")
# MyUtils.log(f'LocalVideo:{LocalVideoSpectrum.length()} LocalUser:{LocalUserSpectrum.length()} Failed:{Failed.length()}')
end()
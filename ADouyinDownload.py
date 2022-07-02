import os.path
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By

import Maintainace
import MyUtils
import DouyinUtils

# 下载
def Download():
    stole=MyUtils.settime()
    global DouyinSum
    # MyUtils.log('[Download] Func Begin')
    while len(ReadyToDownload):
        (VideoNum,(HostID, title, VideoUrl)) = ReadyToDownload.popitem()
        # MyUtils.log(f'VideoNum={VideoNum} HostID={HostID} title={title} VideoUrl={VideoUrl}')
        if not len(VideoUrl)>1:
            # 视频
            path = '../抖音/' + HostID
            # MyUtils.log(f'开始下载，url={VideoUrl[0]}')
            t=MyUtils.MyPageDownload(url=VideoUrl[0],path= f'{path}/{title}.mp4')
        else:
            # 图文
            path = '../抖音/' + HostID
            t=True
            i=0
            for url in VideoUrl:
                i+=1
                # MyUtils.log(f'开始下载，url={url}')
                t=MyUtils.MyPageDownload(url=url,path= f'{path}/{title}/{i}.png')
        if t:
            LocalVideoSpectrum.add(VideoNum)
            MyUtils.log(f'{MyUtils.MyTime("hms")}\n[Download]下载成功，{VideoNum}记录补全.')
            MyUtils.log(f'{DouyinSum}]{HostID}  :',f'作品编号：{VideoNum}     作品标题：{title}\n{VideoUrl}')
            DouyinSum += 1
        else:
            Failed.add(title + '.mp4.crdownload')
            MyUtils.log(f'下载失败，记录增加')

    MyUtils.log(f'{MyUtils.calltime(stole)}s')


# 下载页获取参数
def detect(path,HostID,VideoNum,l):
    stole=MyUtils.settime()
    element=l[0]
    # MyUtils.log('Func Begin')
    # MyUtils.log(isFull)
    index=isFull.index(0)
    isFull[index]=1
    page=PageRe[index]
    # MyUtils.log(f' trying to get {f"https://www.douyin.com/video/{VideoNum}"} ...')

    # 判断是图文
    flag=DouyinUtils.IsPic([element])
    # MyUtils.log(f' flag={flag} VideoNum={VideoNum}')
    if flag:
        page.get(f'https://www.douyin.com/note/{VideoNum}')
        # 删除已经存在的.mp4（以前误下载的）
    else:
        # 判断是视频
        page.get(f'https://www.douyin.com/video/{VideoNum}')
    time.sleep(2)

    # 获取标题
    title=DouyinUtils.Title([page])
    # MyUtils.log(f' title={title}')
    # 如果下载过
    if os.path.exists(f'{path}/{title}.mp4') and not flag:
    #     上面是对图片进行不库判断
    # if os.path.exists(f'{path}/{title}.mp4') and not flag or flag and os.path.exists(f'{path}/{title}'):
        LocalVideoSpectrum.add(VideoNum)
        MyUtils.log(f' Robot{index+1}: {HostID}{title} mp4已存在磁盘中，补全记录')
        isFull[index]=0
        MyUtils.log(f'Robot{index+1} {MyUtils.calltime(stole)}s')
        return

    # 获取下载地址
    VideoUrl=[]
    if not flag:
        VideoUrl = [MyUtils.\
            MyElement(silent=True,l=[page, By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-video-container/video/source[1]'])\
            .get_attribute('src')]
    else:
        elements = MyUtils.MyElements(silent=True,l=[page, By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[1]/div/div[2]/div/img'])
        for e in elements:
            https =e.get_attribute('src')
            VideoUrl.append(https)
    ReadyToDownload.update({VideoNum:(HostID,title,VideoUrl)})
    # MyUtils.log(({VideoNum:(HostID,title,VideoUrl)}))
    # MyUtils.log(f' Robot{index+1}:探测到未下载。准备下载增加，{len(ReadyToDownload)}')
    isFull[index]=0
    MyUtils.log(f'Robot{index+1} {MyUtils.calltime(stole)}s')
    return

def end():
    LocalUserSpectrum.save()
    LocalVideoSpectrum.save()
    MyUtils.log(f'LocalVideo:{LocalVideoSpectrum.length()} LocalUser:{LocalUserSpectrum.length()} Failed:{Failed.length()}')
    DouyinHost.quit()
    sys.exit()
    # VideoPage.set_window_size(900,1000)

# 初始化
Maintainace.Space()
Failed =MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/Failed.txt')
MyUtils.log(f'Failed:{Failed.length()}')
LocalUserSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
LocalVideoSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/VideoSpectrum.txt')
MyUtils.log(f'LocalVideo:{LocalVideoSpectrum.length()} LocalUser:{LocalUserSpectrum.length()} Failed:{Failed.length()}')
UserUID = 1
ReadyToDownload = {}
DouyinSum = 1
maxworkers=5
e=MyUtils.MyPool(maxworkers)
maxworkers1=7
e1=MyUtils.MyPool(maxworkers1)
DouyinHost = MyUtils.MyEdge()
isFull=[0 for i in range(maxworkers)]
UserUID = LocalUserSpectrum.l[0]
DouyinHost.get('https://www.douyin.com/user/' + UserUID.replace('https://www.douyin.com/user/', ''))
e.excute(MyUtils.MyScroll, [DouyinHost])
PageRe=[MyUtils.MyEdge() for i in range(maxworkers)]
while e.cool:
    time.sleep(2)
bbb=False


try:
    while UserUID != None:
        # 用户循环
        UserUID = LocalUserSpectrum.get()


        # 自动去掉UserUID的url前缀
        if UserUID.find('www.douyin.com') > 0:
            LocalUserSpectrum.delete(UserUID)
            UserUID.replace('https://www.douyin.com/user/', '')
            LocalUserSpectrum.add(UserUID)

        # 用户主页处理
        if bbb:
            DouyinHost.get('https://www.douyin.com/user/' + UserUID.replace('https://www.douyin.com/user/', ''))
        MyUtils.MySkip([DouyinHost, By.ID, "captcha-verify-image"])
        # MyUtils.MySkip([DouyinHost, By.ID, "login-pannel"])
        HostID = MyUtils.MyElement([DouyinHost, By.XPATH, '/html/head/title']).get_attribute('text')
        HostID = HostID[0:HostID.rfind('的主页')]
        path = '../抖音/' + HostID
        MyUtils.log(f'  ------已转到{HostID}的主页-----')
        if maxworkers>1 and bbb:
            MyUtils.MyScroll([DouyinHost])
        bbb=True

        try:
            PiecesNum = int(MyUtils.MyElement([DouyinHost, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span']).text)
        except:
            MyUtils.log('https://www.douyin.com/user/' + UserUID)
            LocalUserSpectrum.Rollback()
            input(f'警报。{UserUID}获取作品数目异常。')
            continue


        # 作品列表循环
        for VideolElement in DouyinUtils.HostPieces([DouyinHost]):
            (VideoUrl,VideoNum)=DouyinUtils.Element([VideolElement])
            i = 0

            # 如果下载过
            if (VideoNum in LocalVideoSpectrum.l):
                MyUtils.log(f'{HostID}的作品[{VideoNum}]在记录中，跳过')
                continue

            #     同时进行请求队列减速
            depth=0
            while isFull==[1 for i in range(maxworkers)]:
                MyUtils.log(f'detect队列已满 预备下载队列长度{len(ReadyToDownload)} detect队列实时工作{e.cool} / {e.max_workers}')
                time.sleep(10)
                depth+=1
                if depth>30:
                    MyUtils.log('疑似线程已死亡，主线程开始下载并准备结束。')
                    while len(ReadyToDownload):
                        e1.excute(Download)
                    while e1.cool:
                        time.sleep(10)
                        MyUtils.log(f'等待最后的下载队列完毕。len(ReadtToDownload):{len(ReadyToDownload)}, e.cool:{e.cool}')
                    # 结束
                    LocalVideoSpectrum.save()
                    MyUtils.log('LocalVideo: ', LocalVideoSpectrum.length(), ' LocalUser: ', LocalUserSpectrum.length(), f'Failed:{Failed.length()}')
                    DouyinHost.quit()
                    sys.exit()
            e.excute(detect,path,HostID,VideoNum,[VideolElement])
            MyUtils.log(f'预备下载队列长度{len(ReadyToDownload)}  download队列实时工作{e1.cool}/{e1.max_workers}')
            while len(ReadyToDownload)>maxworkers1:
                while not e1.isFulling():
                    e1.excute(Download)
                    MyUtils.log(f'下载工作数：{e1.cool}  /{len(ReadyToDownload)}')
                    time.sleep(10)

        # 等待下载完成
        # while e1.cool>maxworkers or len(ReadyToDownload)>maxworkers1*2:
        depth=0
        while e1.cool>3 or len(ReadyToDownload):
            if not e1.isFulling():
                e1.excute(Download)
            MyUtils.log(f'等待{HostID}下载队列完成，实时工作数：{e1.cool} / 最大容量：{e1.max_workers} / 剩余任务数：{len(ReadyToDownload)}')
            time.sleep(10)
            if e1.cool<3:
                depth+=1
            if depth>30:
                MyUtils.log('下载队列好像异常了')
                break
        LocalVideoSpectrum.save()
        MyUtils.log(f"用户{HostID}已完成  剩余User总量{LocalUserSpectrum.loopcount}/{LocalUserSpectrum.length()}]")
    # MyUtils.log(f'LocalVideo:{LocalVideoSpectrum.length()} LocalUser:{LocalUserSpectrum.length()} Failed:{Failed.length()}')

finally:
    end()

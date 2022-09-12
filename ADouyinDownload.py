import asyncio
import os.path
import sys
import time
import multiprocessing

from selenium.webdriver.common.by import By

import DouyinUtils
import MyUtils

def download():
    # 变量
    Failed =DouyinUtils.failed
    allpieces=DouyinUtils.allpieces
    readytoDownload=DouyinUtils.readytodownload

    # 下载
    while True:
        stole = MyUtils.nowstr()
        # 获取参数
        # region
        rec=readytoDownload.get()
        if rec==None:
            return
        (VideoNum, author, title, VideoUrl, flag) = rec["list"]
        path = '../抖音/' + author
        MyUtils.delog(f'VideoNum={VideoNum} HostID={author} title={title} VideoUrl={VideoUrl}')
        # endregion
        # 判断是否图文
        if not len(VideoUrl) > 1:
            # 视频
            # region
            MyUtils.delog(f'开始下载，url={VideoUrl[0]}')
            try:
                t = MyUtils.pagedownload(url=VideoUrl[0], path=f'{path}/{title}.mp4',t=15)
            except Exception as e:
                MyUtils.warn(e)
                t = False
            #     endregion
        else:
            # 图片
            # region
            t = True
            i = 0
            for url in VideoUrl:
                i += 1
                MyUtils.delog(f'开始下载，url={url}')
                try:
                    t = MyUtils.pagedownload(url=url, path=f'{path}/{title}/{i}.png',t=0) and t
                except Exception as e:
                    MyUtils.warn(e)
                    t = False
            #     endregion

        # 是否下载成功
        if t:
            # region
            allpieces.add(DouyinUtils.simplinfo(VideoNum, author, title))
            MyUtils.log(f'下载成功，{VideoNum}记录补全.\n{allpieces}]{author}  :作品编号：{VideoNum}     作品标题：{title}\n{VideoUrl}')
            # endregion
        else:
            # region
            Failed.add(DouyinUtils.simplinfo(VideoNum, author, title))
            MyUtils.warn(f'下载失败，{VideoNum} 记录补全到 {Failed.path}.{author} 的编号:{VideoNum} 标题:{title}\n{VideoUrl}')
        MyUtils.log(f'cost{MyUtils.counttime(stole)}')
        # endregion


# 持续性唤醒
while True:
    download()
    MyUtils.log(f'下载队列已空。Downloader 等待中...')
    time.sleep(15)




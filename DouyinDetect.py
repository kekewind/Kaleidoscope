import asyncio
import os.path
import sys
import time
import multiprocessing
from retrying import retry
from selenium.webdriver.common.by import By

import DouyinUtils
import MDouyin
import Maintainace
import MyUtils

# 变量
users = DouyinUtils.allusers
allpieces = DouyinUtils.allpieces
readytodownload = DouyinUtils.readytodownload
ExceptionUser = MyUtils.txt('/抖音/FailedUsers.txt')


@retry(retry_on_exception=MyUtils.retry)
def main():
    # 变量
    Host = MyUtils.chrome()
    page = MyUtils.chrome()
    useruid = 'nothing'

    def detect():
        # 探测
        stole = MyUtils.nowstr()
        # 获取参数
        # region
        flag = DouyinUtils.IsPic([VideoElement])
        # endregion

        # 作品网页
        page.get(elementurl)
        MyUtils.delog(f' 探测 {elementurl} ...')
        MyUtils.skip([page, By.ID, "captcha-verify-image"], strict=True)

        # 获取参数-标题
        # region
        title = DouyinUtils.Title([page])
        MyUtils.delog(f' title={title}')
        # endregion

        # 如果当前操作磁盘里有，增加记录
        # region
        if DouyinUtils.skipdownloaded(flag, allpieces, VideoNum, title, author):
            MyUtils.log(f'{MyUtils.counttime(stole)}s')
            return
        # endregion

        # 获取下载地址
        time.sleep(1)
        DouyinUtils.load(flag, page, VideoNum, author, title, readytodownload)
        MyUtils.log(f'{MyUtils.counttime(stole)}s')

    # 开始用户循环
    while useruid:
        User = users.get()[0]
        fffff = MyUtils.txt('D:/Kaleidoscope/抖音/History.txt')
        fffff.add(str(User))
        useruid = list(User.keys())[0]

        # 清除UserUID的https://www.douyin.com/user/前缀
        # region
        if useruid.find('www.douyin.com') > 0:
            users.delete(useruid)
            useruid.replace('https://www.douyin.com/user/', '')
            users.add(useruid)
        # endregion

        # 用户主页
        # region
        HostUrl = 'https://www.douyin.com/user/' + useruid.replace('https://www.douyin.com/user/', '')
        Host.get(HostUrl)
        # 为什么这句会有两次import输出？？？
        # endregion
        # 获取变量
        # region
        MyUtils.skip([Host, By.ID, "captcha-verify-image"], True)
        MyUtils.skip([Host, By.ID, "login-pannel"])
        author = MyUtils.Element([Host, By.XPATH, '/html/head/title']).get_attribute('text')
        author = author[0:author.rfind('的主页')]
        DouyinUtils.addauthor(useruid, author, users)
        #     continue
        MyUtils.log(f'  ------转到{author}的主页-----')
        MyUtils.delog(HostUrl)
        douyinSum = 0
        PiecesNum = DouyinUtils.HostPiecesNum([Host])
        if PiecesNum == 0:
            ExceptionUser.add(useruid)
            continue
        # endregion
        # 滑动滑块
        # region
        MyUtils.scroll([Host])
        # endregion
        # 获取变量
        # region
        # endregion

        # 作品列表循环
        for VideoElement in DouyinUtils.HostPieces([Host]):
            # 获取变量
            # region
            (elementurl, VideoNum) = DouyinUtils.piecetourlnum([VideoElement])
            # endregion

            # 跳过已下载
            # region
            if DouyinUtils.skiprecorded(VideoNum):
                continue
            # endregion
            detect()
            douyinSum += 1

            #     持续性休眠
            while readytodownload.length() > 5:
                MyUtils.log('下载队列已满。Detect 等待中...')
                time.sleep(10)

    # 结束
    # region
    #     endregion


if __name__ == '__main__':
    main()

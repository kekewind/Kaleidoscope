import MyUtils
import time
import multiprocessing
import TUtils

from selenium.webdriver.common.by import By
from retrying import retry

# 变量
users = TUtils.allusers
allpieces = TUtils.allpieces
readytodownload = TUtils.readytodownload
ExceptionUser = MyUtils.txt('/tiktok/FailedUsers.txt')


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
        # flag = TUtils.IsPic([VideoElement])
        flag = False
        # endregion

        # 作品网页
        page.get(elementurl)
        MyUtils.delog(f' 探测 {elementurl} ...')
        MyUtils.skip([page, By.ID, "captcha-verify-image"], strict=True)

        # 获取参数-标题
        # region
        s = TUtils.Title([page])
        title = s[:s.find('  採用')]
        MyUtils.delog(f' title={title}')
        # endregion

        # 如果当前操作磁盘里有，增加记录
        # region
        if TUtils.skipdownloaded(flag, allpieces, VideoNum, title, author):
            MyUtils.log(f'{MyUtils.counttime(stole)}s')
            return
        # endregion

        # 获取下载地址
        time.sleep(1)
        TUtils.load(flag, page, VideoNum, author, title, readytodownload)
        MyUtils.log(f'{MyUtils.counttime(stole)}s')

    # 开始用户循环
    while useruid:
        User = users.get()
        useruid = MyUtils.key(User)

        # 用户主页
        # region
        HostUrl = 'https://www.tiktok.com/@' + useruid
        Host.get(HostUrl)
        # endregion
        # 获取变量
        # region
        # MyUtils.skip([Host, By.ID, "captcha-verify-image"], True)
        # MyUtils.skip([Host, By.ID, "login-pannel"])
        s = Host.title
        author = s[:s.rfind(' (@')].strip('\t')
        TUtils.addauthor(useruid, author, users)
        # if author in TUtils.diskusers:
        #     MyUtils.delog(f'当前用户{author}在操作盘中，跳过')
        #     continue
        MyUtils.log(f'  ------转到{author}的主页-----')
        MyUtils.delog(HostUrl)
        tiktokSum = 0
        # endregion
        # 滑动滑块
        # region
        MyUtils.scroll([Host])
        # endregion

        # 作品列表循环
        for VideoElement in TUtils.HostPieces([Host]):
            # 获取变量
            # region
            (elementurl, VideoNum) = TUtils.piecetourlnum([VideoElement])
            # endregion

            # 跳过已下载
            # region
            if TUtils.skiprecorded(VideoNum):
                continue
            # endregion
            detect()
            tiktokSum += 1

            #     持续性休眠
            while readytodownload.length() > 5:
                MyUtils.log('下载队列已满。Detect 等待中...')
                time.sleep(10)
        allpieces.save()

    # 结束
    # region
    allpieces.save()
    #     endregion


if __name__ == '__main__':
    main()

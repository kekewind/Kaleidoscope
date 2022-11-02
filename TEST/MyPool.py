import concurrent.futures
import requests
import time
import MyUtils

a = MyUtils.txt(MyUtils.desktoppath('0'))


@MyUtils.listed
def funfromurl(b, c):
    print(f'{b}, time {c}')
    # page=MyUtils.Chrome()
    time.sleep(10)


def download_many(sites):
    e = MyUtils.pool(40)
    for site in sites:
        # e.doorwait(funfromurl, [(site,'wwww'),(site,'ssss')])
        e.doorwait(funfromurl, site, [1, 2, 3])


def main():
    sites = [
        'https://www.baidu.com',
        'https://www.zhihu.com',
        'https://www.taobao.com',
        'https://www.douban.com',
        'https://www.jianshu.com',
        'https://account.geekbang.org',
        'https://leetcode-cn.com/',
        'https://www.github.com',
        'https://open.163.com/',
        'https://www.rainymood.com/',
        'https://www.bilibili.com/',
    ]
    download_many(sites)


if __name__ == "__main__":
    main()

import concurrent.futures
import requests
import time

import MyUtils


def download_one(site):
    resp = requests.get(site)
    print('Read {} from {}'.format(len(resp.content), site))
    time.sleep(10)


def download_many(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for site in sites:
            executor.submit(download_one, site)


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
    start = time.time()
    download_many(sites)
    end = time.time()
    print('Download {} sites by {}s'.format(len(sites), end - start))


if __name__ == "__main__":
    main()

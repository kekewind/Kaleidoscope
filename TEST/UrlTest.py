import time

import MyUtils

url = 'https://v26-web.douyinvod.com/2206bc9282ca50e1a6c28b36e8342df8/62bd392a/video/tos/cn/tos-cn-ve-15/09c760de493d443aaee704c7d82506bc/?a=6383&ch=26&cr=0&dr=0&lr=all&cd=0%7C0%7C0%7C0&cv=1&br=796&bt=796&cs=0&ds=6&ft=5q_lc5mmnPD12N6Owy.-UxPTFaY3c3wv25Ha&mime_type=video_mp4&qs=0&rc=aDVkNmgzMzk3ZTk0ZTxpOUBpamt1NWxzZTk8dzMzZGkzM0A2Ly80MDAuXzIxXzRjYl9hYSNrcWpzZ2VmamJfLS00LS9zcw%3D%3D&l=021656564463774fdbddc0200ff2f010a9e5e850000012525fa7c'
# MyUtils.MyPageDownload(url=url,path=MyUtils.DesktopPath('1.mp4'))
a = MyUtils.chrome(url)
time.sleep(50)

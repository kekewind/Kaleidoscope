import time

import MyUtils


def fo(n):
    # print('start')
    stole = MyUtils.recordtime()
    print(n, stole)
    MyUtils.dosth()
    print(MyUtils.counttime(stole))


e = MyUtils.MyThreadPool(5)
i = 0
while True:
    i += 1
    while not e.isFulling():
        e.excute(fo, i)
        time.sleep(1)
    if i > 100:
        break

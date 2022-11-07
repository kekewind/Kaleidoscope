# 每二十分钟改变鼠标位置来提醒需要记录了
# 如果一个时间内没有记录，则记为空；
# 在下一次记录返回后，先记录本次，再依次询问之前的记录补全
import time

import pyperclip
import MyUtils


def next(t):
    while not MyUtils.now().minute in [0, 20, 40, 60]:
        time.sleep(59)
    MyUtils.WARN(f'请前往记录。<A20min>')
    ret = '\n' + MyUtils.realtime()[:-3]
    t.add(ret)
    time.sleep(59 * 2)
    return ret.strip('\n')


def main():
    while True:
        t = MyUtils.txt(f'D:/Kaleidoscope/self/20MINUTES/{MyUtils.today()}.txt')
        # t = MyUtils.txt(MyUtils.desktoppath('0.txt'))
        # if not MyUtils.now().minute in [0,20,40,60]:
        #     time.sleep(60)
        #     continue
        c = input(f'请输入{next(t)}')
        t.add(c)


if __name__ == '__main__':
    main()

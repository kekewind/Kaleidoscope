# 不断读入
# 每二十分钟存记录一次
import pyperclip

import MyUtils
import time

cc = ''
f=MyUtils.MyTXT(MyUtils.MyPath('D:/Kaleidoscope/self/20MINUTES/'+MyUtils.MyDate('.txt')))
c=[]

def record():
    while True:
        print('[record] begin')
        global c
        cc=input()
        c.append(cc)
        print('[record] end')

def writedown():
    while True:
        print('[writedown] begin')
        global c,f
        if not MyUtils.MyTime('m')in['0','00','20','40']:
            time.sleep(20*60)
            continue
        f.add(MyUtils.MyTime('hm'))
        pyperclip.copy(f)
        for i in c:
            f.add(i)
            print(f'i={i}')
        c=[]
        f.save()
        print('[writedown] end')


e1=MyUtils.MyThreadPool(2)
e2=MyUtils.MyThreadPool(2)
e1.excute(record)
e1.excute(writedown)

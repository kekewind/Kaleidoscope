import time

import MyUtils

f = MyUtils.cache(MyUtils.DesktopPath('ab.txt'))

while True:
    f.add({'a': MyUtils.nowstr()})
    time.sleep(5)

while True:
    time.sleep(1)
    print(f.get())

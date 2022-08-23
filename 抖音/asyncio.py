import time

import MyUtils
a=MyUtils.RefreshJson(MyUtils.DesktopPath('b.txt'))
i=0
while True:
    i+=1
    a.add({f"{i}":2})
    time.sleep(1)
    print(len(a.l))
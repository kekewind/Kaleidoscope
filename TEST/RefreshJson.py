import time

import MyUtils
import DouyinUtils

f = DouyinUtils.allpieces
f1 = MyUtils.RefreshJson(MyUtils.DesktopPath('b.txt'))
f1.add({"5": 1})
print(f1.l)
time.sleep(9999)

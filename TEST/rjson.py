import time

import MyUtils

f = MyUtils.rjson(MyUtils.desktoppath('b'))
# for i in range(10):
print(f.get())
print('#')
print(f.rollback())

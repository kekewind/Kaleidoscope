import time

import MyUtils

# page=MyUtils.edge()
page = MyUtils.Edge()
print(type(page))
page.open('www.baidu.com')
time.sleep(9999)

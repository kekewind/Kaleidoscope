import time

import MyUtils


@retry
def do(a, b, c=0):
    MyUtils.delog('a')
    print(a, b, c)
    page = MyUtils.edge()
    raise ConnectionRefusedError
    MyUtils.delog('z')


print(do(3, 4, c=1))

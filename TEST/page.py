import time

import MyUtils


def fun():
    page = MyUtils.Chrome('https://www.baidu.com', silent=False)
    MyUtils.sleep(10)


def main():
    fun()


if __name__ == '__main__':
    main()

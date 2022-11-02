import time

import MyUtils


def fun():
    page = MyUtils.Chrome('https://www.baidu.com', silent=True)
    MyUtils.sleep()


def main():
    fun()


if __name__ == '__main__':
    main()

import time

import MyUtils


def main():
    @MyUtils.consume
    def fun(a):
        time.sleep(1)
        print(a)

    fun(1)


main()

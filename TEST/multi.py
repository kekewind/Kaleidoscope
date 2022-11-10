import multiprocessing
import time


def func(a, b=1, c=1):
    while True:
        print(a, b, c)
        time.sleep(0.9)


def main():
    pool1 = multiprocessing.Pool(1)
    for i in range(15):
        pool1.apply_async(func, args=(1,), kwds={'b': 2, 'c': 3})
    pool1.close()
    pool1.join()

# close,joinpool和函数声明位置必须与上面保持一致,Pool的声明至少要在一个函数中而不是外部。
if __name__ == '__main__':
    main()

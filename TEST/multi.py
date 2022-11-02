import multiprocessing
import time


def func(a, b=1, c=1):
    print(a, b, c)


if __name__ == '__main__':
    pool1 = multiprocessing.Pool(3)
    for i in range(15):
        pool1.apply_async(func, args=(1,), kwds={'b': 2, 'c': 3})
    pool1.close()
    pool1.join()

# close,joinpool和函数声明位置必须与上面保持一致,。

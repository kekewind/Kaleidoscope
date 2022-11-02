import inspect


def fun():
    print(inspect.getframeinfo(inspect.currentframe()))
    print(inspect.getframeinfo(inspect.currentframe().f_back))


if __name__ == '__main__':
    fun()

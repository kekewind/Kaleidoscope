import retrying
import MyUtils


def p():
    pass


try:
    print('s' * 2 + 1)
except Exception as e:
    MyUtils.retry()
    print(e)

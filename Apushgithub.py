import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    # 持续推送到github
    while True:
        MyUtils.CMD(f'cd d:;cd {MyUtils.projectpath()};git push',silent=True)
        time.sleep(60*5)


import time

import MyUtils
import YUtils
import pyautogui
import time


def main():
    time.sleep(2)
    path = MyUtils.desktoppath('111.png')
    pos = pyautogui.locateOnScreen(path)
    print(pos)
    pyautogui.center(pos)


if __name__ == '__main__':
    main()

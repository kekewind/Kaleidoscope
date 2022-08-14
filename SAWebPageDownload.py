import time

import pyperclip

import MyUtils
import pyautogui

pyperclip.copy(input("输入路径："))
time.sleep(0)
# 转到网页
pyautogui.hotkey('alt','tab')
time.sleep(2)

# 保存
pyautogui.hotkey('ctrl', 'l', duration=1)
time.sleep(5)
# 输入网址
pyautogui.click(570, 101)
time.sleep(1)
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)
pyautogui.hotkey('enter')
time.sleep(1)
pyautogui.click(712, 982)
time.sleep(1)
pyautogui.hotkey('ctrl', 'w', duration=1)
time.sleep(2)

while True:
    # 保存
    pyautogui.hotkey('ctrl','l',duration=1)
    time.sleep(5)
    pyautogui.hotkey('enter',duration=1)
    time.sleep(1)
    pyautogui.hotkey('ctrl','w',duration=1)
    time.sleep(2)
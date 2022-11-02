import time

import pyautogui
import selenium.webdriver

Page = selenium.webdriver.Edge()
Page.get('http://www.ab173.com/other/huaban.php')
# Page.get('https://pbs.twimg.com/media/FHSlTH2XoAwXlol?format=jpg&name=small')
# Page.set_window_size(100,100)
time.sleep(0.2)
pyautogui.mouseDown(256, 596)
pyautogui.moveTo(321, 600)
pyautogui.mouseUp()
time.sleep(0.2)
time.sleep(1000)

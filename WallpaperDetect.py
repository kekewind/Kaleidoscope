import time

import pyautogui
import pyperclip

import MyUtils
import WallpaperUtils
readytodownload=WallpaperUtils.readytodownload
def fun():
    pass

# 对wallpaper网站进行最大化后自动化，alt+tab，点击复制网址，关闭网页，依次加入到txt
def main():
    fun()
    while True:
        # 复制网址并关闭网页
        pyautogui.hotkey('alt','tab')
        pyautogui.click(1075,72)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl','c')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl','w')
        readytodownload.add(pyperclip.paste())
        break






if __name__ == '__main__':
    main()
    page=MyUtils.Chrome(silent=True)

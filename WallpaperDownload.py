import MyUtils
import WallpaperUtils

def fun():

    page.get(pyperclip.paste())
    readytodownload.add(page.element('//*[@id="wallpaper"]').get_attribute('src'))

# 后台下载到图片/未分类
def main():
    fun()



if __name__ == '__main__':
    main()

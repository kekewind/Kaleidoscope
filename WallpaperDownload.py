import MyUtils
import WallpaperUtils
import pyperclip
import WallpaperUtils
readytodownload=WallpaperUtils.readytodownload



# 后台下载到图片/未分类
page = MyUtils.Chrome(silent=True)
def fun():
    path=f'C:/{MyUtils.user}/Pictures/WallPaper/static/未分类'
#     开始下载
    url=MyUtils.value(readytodownload.get())[0]
    while not url==None:
        page.get(url)
        url=(page.element('//*[@id="wallpaper"]').get_attribute('src'))
        MyUtils.pagedownload(url,f'{path}/{MyUtils.tail("/")}',t=3)
        url=readytodownload.get()


def main():
    fun()



if __name__ == '__main__':
    main()

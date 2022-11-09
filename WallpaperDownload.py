import MyUtils
import WallpaperUtils
import pyperclip
import WallpaperUtils
readytodownload=WallpaperUtils.readytodownload



# 后台下载到图片/未分类
page = MyUtils.Chrome(silent=True)
def fun():
    path=f'C:/Users/{MyUtils.user}/Pictures/WallPaper/static/未分类'
#     开始下载
    url=MyUtils.value(readytodownload.get())[0]
    while not url==None:
        page.get(url)
        durl=(page.element('//*[@id="wallpaper"]').get_attribute('src'))
        if not MyUtils.pagedownload(durl,f'{path}/{MyUtils.tail(durl,"/")}',t=2):
            MyUtils.Exit(url)
        url=MyUtils.value(readytodownload.get())[0]
        MyUtils.delog(url)


def main():
    fun()



if __name__ == '__main__':
    main()

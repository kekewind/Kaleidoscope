import os
import time
from selenium.webdriver.common.by import By
import selenium.webdriver.remote.webelement
import MyUtils

droot='../QQ/QSpace/'
User=MyUtils.RefreshTXT(droot+'User.txt')
# page=MyUtils.MyEdge(show=True)
page=MyUtils.chrome()
page.set_window_size(1920,1080)
e=MyUtils.MyThreadPool(20, show=1)
b=True
while User.loopcount<User.length():
    qq=User.get()
    MyUtils.CreatePath(droot + qq)
    print('[Main] 前往页面中')
    page.get('https://user.qzone.qq.com/' + qq)
    time.sleep(2)
    if b:
        page.switch_to.frame(MyUtils.Element([page, By.TAG_NAME, 'iframe']))
        # MyUtils.MyElement([page,By.XPATH,'/html/body/div[1]/div[4]/div[8]/div/span/span[1]']).screenshot(MyUtils.DesktopPath('login.png'))
        name=time.time()
        print('[Main] 下载二维码中')
        MyUtils.MyScreenShot(MyUtils.PicCachePath(f'{name}.png'),[page],whole=1,show=1)
        print('[Main] 二维码下载完成')
        MyUtils.deletedirandfile(MyUtils.PicCachePath(f'{name}.png'))
        page.switch_to.default_content()
        # MyUtils.MySkip([page,By.ID,'qrlogin_img'])
        MyUtils.skip([page, By.ID, 'login_frame'])
        time.sleep(3)
        b=False
    page.set_window_size(1920, 9999)
    MyUtils.scroll([page])
    page.switch_to.frame(MyUtils.Element([page, By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/iframe']))
    lis=MyUtils.Elements([page, By.XPATH, '/html/body/div[1]/div[1]/ul/li'])
    for element in lis:
        name=MyUtils.MyName(element.text)
        name=name[:name.rfind('浏览')]
        name=name.replace(' ','')
        print(f'[Main] {name}')
        # 判断是否重合
        # if MyUtils.MyPathExist(droot+qq,name,ratio=1):
        #     print(name+' 已下载')
        #     continue
        MyUtils.CreatePath(droot + qq + '/' + name)



        #     获取tweet截屏
        # MyUtils.MyScreenShot(element=element,show=1,path=droot+qq+'/'+name+f'/Overall.png')

        # 获取内含视频/图片
        imglist=MyUtils.Elements([element, By.CLASS_NAME, 'img-item  '])
        j=0
        for img in imglist:
            j+=1
            def geturl(element):
                list=['data-pickey','data-v_vidioswfurl','data-originurl']
                k=''
                while k.find('://') < 1:
                    while list==[]:
                        time.sleep(5)
                    ee = element.get_attribute(list.pop(0))
                    k = ee[ee.find(',') + 1:]
                    print(f'[geturl] k={k}')
                return k
            url=geturl(img)
            print('[Main] 已获得资源地址',url)
            try:
                while e.isFulling():
                    time.sleep(2)
                e.excute(MyUtils.pagedownload, url, droot + qq + '/' + name + f'/{j}.jpg')
                print('[Main] 已提交图片地址',url)
            except:
                while e.isFulling():
                    time.sleep(2)
                e.excute(MyUtils.pagedownload, url, droot + qq + '/' + name + f'/{j}.mp4')
                print('[Main] 已提交视频地址',url)

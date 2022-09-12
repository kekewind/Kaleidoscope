import os
import shutil
import time

import MyUtils
from selenium.webdriver.common.by import By


# 抖音，去掉- 抖音结尾的mp4，并且重命名
def douyin1():
    l=[]
    for(root,dirs,files)in os.walk('../抖音/'):
        # 遍历每个文件夹
        for dir in dirs:
            for (root,dirs,files)in os.walk(f'../抖音/{dir}'):
                for file in files:
                    # 遍历每个MP4
                    if file.find(' - 抖音.mp4')>0:
                        path=os.path.abspath(f'{root}/{file}')
                        # 如果已存在没有- 抖音的视频，也就是说两个，那先跳过，后面再删除多余的那个
                        if os.path.exists(path.strip(' - 抖音.mp4')+'.mp4'):
                            l.append(path)
                        else:
                            os.rename(path,path.strip(' - 抖音.mp4')+'.mp4')
            print(f'{dir} checked.')
    # 删除多余的那个
    MyUtils.deletedirandfile(l)

# 对为下载完成文件
def douyin2():
    newfile=MyUtils.RefreshTXT('../抖音/FailedPieces.txt')
    page=MyUtils.edge()
    l=[]
    for(root,dirs,files)in os.walk('../抖音/'):
        # 遍历每个文件夹
        for dir in dirs:
            for (root,dirs,files)in os.walk(f'../抖音/{dir}'):
                for file in files:
                    # 遍历每个MP4，对于未下载完成文件
                    if file.find('.mp4.crdownload')>0:
                        # Name=dir+' '+file.replace('#','%23').strip('.mp4.crdownload')
                        # page.get('https://www.douyin.com/search/'+Name)
                        # # 检查第一个搜索结果用户名对不对
                        # userid=MyUtils.MyElement([page,By.XPATH,'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/ul/li[1]/div/div/div[1]/div/div/div[1]/a/p/span/span/span/span/span']).text
                        # if userid!=dir:
                        #     continue
                        # 准备删除原文件，并记录到Fail
                        l.append(os.path.abspath(f'{root}/{file}'))
                        newfile.add(f'{dir}{file}')
    MyUtils.deletedirandfile(l)
    if not len(l):
        os.remove('../抖音/VideoSpectrum.txt')

# 把like里面的标题全部check，搜索，搜索到第一个符合文案的结果，获取用户ID，转移文件到文件夹中
def douyin3():
    page=MyUtils.edge('https://www.douyin.com')
    for (root,dirs,files)in os.walk('../抖音/like'):
        for file in files:
            # 跳过
            MyUtils.skip([page, By.ID, "captcha-verify-image"],True)
            MyUtils.skip([page, By.ID, "login-pannel"])
            time.sleep(1)

            MyUtils.MyKeyInput(323,233,file.strip('.mp4'))
            time.sleep(1)
            element=MyUtils.Element([page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[1]/ul/li[1]/div/div/div[1]/div/a'])
            UserUID=element.get_attribute('href')
            UserUID=UserUID[UserUID.find('user/'):UserUID.find('?')]
            time.sleep(1)


def douyin5():
#     维护Failed.txt，删除已经不必要存在的.crdownload
    lis=[]
    deletelis=[]
    f=MyUtils.RefreshTXT('../抖音/FailedPieces.txt')
    for (root,dirs,files)in os.walk('../抖音'):
        for dir in dirs:
            for (root1,dirs1,files1)in os.walk(f'../抖音/{dir}'):
                for file in files1:
                    if not 0<file.find('.crdownload') < 3:
                        lis.append(file)
                    else:
                        deletelis.append(os.path.abspath(f'../抖音/{dir}/{file}'))
                        f.add(file)
                        print(f'准备删除.crdownload文件{file}')

    MyUtils.deletedirandfile(deletelis)

    while f.loopcount<f.length():
        a=f.get()
        aa=a.strip('.crdownload')
#         如果后来下载成功了
        if aa in lis:
            f.delete(a)
            print(f'记录{a}删除.')

def douyin6():
#     统计记录的数目
    Failed = MyUtils.RefreshTXT('../抖音/FailedPieces.txt')
    print(f'Failed:{Failed.length()}')
    LocalUserSpectrum = MyUtils.RefreshTXT('../抖音/AllUsers.txt')
    LocalVideoSpectrum = MyUtils.RefreshTXT('../抖音/VideoSpectrum.txt')
    print('LocalVideo: ', LocalVideoSpectrum.length(), ' LocalUser: ', LocalUserSpectrum.length())
def SeleniumSpace(silent=True):
    dlis=[]
    for dir in os.listdir('C:\\Users\\17371\\AppData\\Local\\Temp'):
        if dir.find('scoped_dir')>=0:
            dlis.append('C:\\Users\\17371\\AppData\\Local\\Temp\\'+dir)
            if len(dlis)>500:
                MyUtils.deletedirandfile(dlis, silent=True)
                dlis=[]
    MyUtils.deletedirandfile(dlis, silent=True)

def storagemove():
    for i in MyUtils.listfile('D:/'):
        ex=MyUtils.filename(i)
        ex=MyUtils.tail(ex,'.')
#         如果是视频
        if ex in ['mp4']:
            shutil.move(i,f'./storage/未分类视频/{MyUtils.filename(i)}')
            # print((i,f'./storage/视频/{MyUtils.filename(i)}'))
        if ex in ['jpg','jpeg','png','webp']:
            shutil.move(i,f'C:/Users/17371/Pictures/未分类/{MyUtils.filename(i)}')

#     author错位
def douyin7():
    l=[]
    d={}
    sum=0
    OverwhelmedSize=0
    for (root,dirs,files)in os.walk('../抖音'):
        for file in files:
            # 先拼路径
            path=MyUtils.standarlizedPath(root + '/' + file)
            stat_info=os.stat(path)
            size=stat_info.st_size
            d.update({file:size})
            if not file in l:
                l.append(file)
                d.update({file:size})
            else:
                sum+=1
                print(path,size)
                OverwhelmedSize+=size
    print('检测到的重复名字的文件/总文件个数：')
    print(sum,'/',len(l),'总大小：',(OverwhelmedSize//1024)//1024//1024,'GB')

def douyin8():
#     回退库存
    l=[]
    for (root,dirs,files)in os.walk('../抖音'):
        break
    for dir in dirs:
        for (root,dirs1,files)in os.walk(f'../抖音/{dir}'):
            for file in files:
                t=os.path.getctime(os.path.abspath(f'../抖音/{dir}/{file}'))
                if t>999999999999999999999:
                    l.append(os.path.abspath(f'../抖音/{dir}/{file}'))
    MyUtils.deletedirandfile(l)

# douyin2()
# douyin1()
# douyin3()
# douyin4()
# douyin5()
# douyin6()
# douyin7()
# douyin8()

# douyin6()

#反向从操作盘中检查申明
def checkisindisk(record,func,):
    length1=record.length()
    for i in record.l:
        d1=MyUtils.jsontodict(i)
        uid=list(d1.keys())[0]
        d=d1.get(uid)
        author=d['author']
        title=d['title']
        if d['disk']==MyUtils.diskname:
            if func((uid,author,title,d1,d)):
                continue
            else:
                record.delete(d1)
    MyUtils.log(f'{length1}->{record.length()}')

# 一般需要的实现（可选）：
# 已下载添加作品记录
# 已下载添加作者记录
# 手动删除作者
# 自动删除作品
# 手动添加作者

# *删除不存在的作品记录
# *统计重复的作品


try:
    SeleniumSpace()
except:
    pass
# storagemove()
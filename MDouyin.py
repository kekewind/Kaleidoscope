import os

import MyUtils
def douyin0():
    rep=MyUtils.RefreshTXT('../抖音/Failed.txt')
    for(root,dirs,files)in os.walk('../抖音'):
        for dir in dirs:
            for (root1,dirs1,files1)in os.walk(f'../抖音/{dir}'):
                for file1 in files1:
                    name=file1.strip('mp4')
                    if name+'.crdownload' in files1:
                        os.remove(os.path.abspath(f'./抖音/{dir}/{name+".crdowanload"}'))
                        print(f'{name} 检测到后来又下载成功了，删除crdownload文件')
                    if file1.find('crdownload')>0:
                        if not file1.strip('.crdownload')in files1:
                            # 新增记录
                            rep.add(file1)
                            print(f'{file1} 检测到有新的下载失败')
    while rep.loopcount<rep.length():
        a=rep.get()
        for (root,dirs,files)in os.walk('../抖音'):
            if a.strip('.crdownload')in files:
                rep.delete(a)
                print(f'{a} 检测到后来又下载成功了，删除记录')

def douyin1():
    # Account异常，对json列表进行手动导入（只导入非0）
    a={}
    a=input()
    a=eval(a)
    l=[]
    txtf=MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
    for key in a.keys():
        if a.get(key)>0:
            l.append(key)
    txtf.add(l)
    txtf.save()

def douyin2():
    # 清除所有的.mp3
    for(root,dirs,files)in os.walk('../抖音'):
        for dir in dirs:
            for (root1,dirs1,files1)in os.walk(f'../抖音/{dir}'):
                for file1 in files1:
                    if file1.find('.mp3')>-1:
                        continue
def douyin3(t):
#     回滚UserList
    for i in range(t):
        f=MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
        f.Rollback()
        f.save()

def douyin4():
#     检查其它盘，非运行盘，进行上网核对，《可能用json》
#     打开txt，获取作品编号
#
    return

def douyin5():
#     输入字符串，正则匹配，去除库里包含的所有作品号
    c='1'
    l=[]
    f=MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/VideoSpectrum.txt')
    while not c=='':
        c=input()
        l.extend(MyUtils.Myre(c,'\d'*19))
    for i in l:
        f.delete(i)
    f.save()

# douyin1()
# douyin2()
douyin3(1)
# douyin5()
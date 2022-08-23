import os

import MyUtils


# Distribute是：
#   1、提供所有记录的最终集合
#   2、提供下载时的判断依据
# 在最后预览使用时，需要一个作者的所有作品都在一起。
# 但是怎么保证移到一起去不会出问题呢？本身一个作者的不断源造成的空间是不可限制的。
# 这一步需要交给人工来做。机器只负责统计每个盘里有多少作者。
# 这一步可以在下载、探测以后独立检测地执行。


#     查看ReadytoDownload数量
def readynum():
    MyUtils.log(MyUtils.txt('D:/Kaleidoscope/抖音/ReadytoDownload.txt').length())

# 由于download-url有问题，进行了误下载。因此清空下载记录和准备下载。
def clearall():
    MyUtils.deletedirandfile('D:/Kaleidoscope/抖音/AllPieces.txt')
    MyUtils.deletedirandfile('D:/Kaleidoscope/抖音/ReadytoDownload.txt')

def clearready():
    MyUtils.deletedirandfile('D:/Kaleidoscope/抖音/ReadytoDownload.txt')

# 检查all里的作品是否在disk内
def checkisindisk():
    e=MyUtils.Json('D:/Kaleidoscope/抖音/missingPieces.txt')
    for i in MyUtils.txt('D:/Kaleidoscope/抖音/AllPieces.txt').l:
        d=MyUtils.jsontodict(i)
        d=d.get(list(d.keys())[0])
        diskname=MyUtils.diskname
        if d['disk']==diskname:
            if os.path.exists(f'./抖音/{d["author"]}/{d["title"]}') or os.path.exists(f'./抖音/{d["author"]}/{d["title"]}.mp4'):
                continue
            else:
                e.add(d)


def douyin3(count):
    #     回滚UserList
    for i in range(count):
        f = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/UserSpectrum.txt')
        f.Rollback()
        f.save()


def douyin4():
    # 输出操作盘里的所有author
    record = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/authorDistribute.txt')
    ret={}
    for (root,dirs,files)in os.walk('./抖音'):
        break
    for author in dirs:
        for (root1,dirs1,files1)in os.walk(f'./抖音/{author}'):
            count=len(dirs1)+len(files1)
            ret.update({author:count})
            break
    record.add({MyUtils.getdiskname():ret})

def douyin5():
    #     输入字符串，正则匹配，去除VideoSpectrum里包含的所有作品号
    c = '1'
    l = []
    f = MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/VideoSpectrum.txt')
    while not c == '':
        c = input()
        l.extend(MyUtils.Myre(c, '\d' * 19))
    for i in l:
        f.delete(i)
    f.save()

def douyin6():
#     对UserList执行从RefreshTXT到Json的重构
    f=MyUtils.txt("D:/Kaleidoscope/抖音/UserSpectrum.txt")
    newl=[]
    for i in f.l:
        newl.append('{\"'+i+'\":[]}')
    f.l=newl
    f.save()

def douyin7():
#     根据All在操作盘中检索，并删除掉没有的记录
    all=MyUtils.RefreshTXT('D:/Kaleidoscope/抖音/AllPieces.txt')
    while True:
        rec=all.get()
        num=list(rec.keys())[0]
        diskname=(rec[num]['disk'])
        author=(rec[num]['author'])
        title=(rec[num]['title'])
        if not os.path.exists(f'./抖音/{author}/{title}'):
            all.delete(rec)

# douyin0()
# douyin1()
# douyin2()
# douyin3(1)
# douyin4()
# douyin5()
# douyin6()
# douyin7()
# checkisindisk()
MyUtils.log(f"记录总长度：{MyUtils.txt('D:/Kaleidoscope/抖音/AllPieces.txt').length()}")
# MyUtils.warn('MDouyin loaded.')
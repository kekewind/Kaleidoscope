import os
import shutil
import sys
import time

import pyperclip
import requests
from selenium.webdriver.common.by import By

import BUtils
import DouyinUtils
import Maintainace
import MyUtils

# 压力测试
# 多作者、多P
# 组织方式约定：
# ./bili/upUID/
#        视频标题_BV********.jpg(png)，
#                 分P标题.MP4，简介内容.txt。字幕文件


# count=MyUtils.RefreshTXT(f'D:/Kaleidoscope/bili/CoverSpectrum.txt')
# path='E:/bili/cover/'
# for i in count.l:
#     id=upid(i)
#     print((id,i))
#     if id==None:
#         count.delete(i)
#         count.save()
#         continue
#     if not os.path.exists(path+id):
#         continue
#     for(root,dirs,files)in os.walk(path+id):
#         inc=0
#         for file in files:
#             if not file.find('jpg'):continue
#             originfile=file
#             file=file[file.find('BV'):-4]
#             ss=''
#             for sss in file:
#                 if '0'<=sss<='9' or 'a'<=sss<='z' or 'A'<=sss<='Z':
#                     ss+=sss
#                     continue
#                 break
#             file=file[len(ss):]
#             file+=ss+'.jpg'
#             MyUtils.MyCreatePath(f'./Bili/{id}_{i}')
#             shutil.move(os.path.abspath(path+id+'\\'+originfile),os.path.abspath(f'./Bili/{id}_{i}/{ss}.jpg'))
#             inc+=1
#             print(f'[Main]{inc}/{len(files)}')
# MyUtils.MyDeleteEmpty('./bili/cover')
#
# # 上面是图片转移的代码,在E盘且在spectrum里的转移并重命名

videospectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoSpectrum.txt')
videouserspectrum=MyUtils.RefreshTXT('D:\Kaleidoscope/bili/VideoUserSpectrum.txt')
videouserexpired=MyUtils.RefreshTXT('D:\Kaleidoscope/bili/VideoUserExpired.txt')

coverspectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/CoverSpectrum.txt')


downloadedindisk=MyUtils.RefreshTXT('./bili/Downloaded.txt')


def upid(UID):
    # 根据数字返回名字
    url = (f'https://api.bilibili.com/x/space/arc/search?mid={UID}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp')
    res = requests.get(url, headers=MyUtils.headers)
    # print(f"[upid] {res.json()['data']}")
    # print(f"[upid] {res.json()['data']['list']['vlist'][0]['author']}")
    try:
        for i in res.json()['data']['list']['vlist']:
            if not i['mid'] == UID:
                continue
            return MyUtils.MyName(i['author'])
    except:
        print(f"[upid] error when trying mid(UID)={UID}")
        return None

# 获取bv
def filenametonum(s):
    if s=='':
        MyUtils.warn()
        sys.exit(-1)
    return s[s.rfind('_')+1:]

# 记录操作盘user、pieces
def makerecord():
    length1=videospectrum.length()
    f=[]
    for i in MyUtils.listdir('./bili'):
        f.append(i[i.rfind('_')+1:])
        for k in MyUtils.listdir(i):
            j=MyUtils.filename(k)
            num=(filenametonum(j))
            title=j[:-len('_'+num)]
            videospectrum.add(DouyinUtils.simplinfo(num,filenametonum(i),title))
    MyUtils.log(['user: ',f])
    downloadedindisk.l=f
    downloadedindisk.save()
    MyUtils.log(f'{length1}->{videospectrum.length()}')

# 打开网页，决定是否要expire
def checkweb():
    page=MyUtils.edge()
    count=0
    for i in range(downloadedindisk.length()):
        num=downloadedindisk.get()
        count+=1
        page.execute_script(f"window.open('https://space.bilibili.com/{num}?')")
        if count>=20:
            break
    expire()

# 立刻从Expired更新UserList
def expire():
    while True:
        num=input('请输入expire编号：')
        num=num.strip('?').strip('https://space.bilibili.com/')
        videouserspectrum.delete(num)
        videouserexpired.add(num)
        MyUtils.log(f'{num} expired.')

# 删除操作盘里的作者文件
def delete():
    lis=[]
    for i in videouserexpired.l:
        dirs=MyUtils.listdir('./bili')
        for k in dirs:
            num=k[k.rfind('_')+1:]
            if num==i:
                lis.append(k)

    print(f'操作盘中存在的作者： {lis}')
    MyUtils.deletedirandfile(lis)

# 立刻命令行添加用户
def add():
    c=input('请输入要添加的用户：')
    MyUtils.log(f'{BUtils.urltouseruid(c)} added.')

#反向从操作盘中检查申明
def checkisindisk():
    def func(tuple):
        (uid,au,ti,d1,d)=tuple
        b=False
        for i in MyUtils.listdir('./bili'):
            if MyUtils.tellstringsame(i,au):
                b=True
                break
        if b==False:
            MyUtils.delog(f'不存在{d}{222}')
            return False
        for j in MyUtils.listdir(i):
            if MyUtils.tellstringsame(MyUtils.filename(j), f'{ti}_{uid}'):
                MyUtils.delog(f'存在{d}')
                return True
        MyUtils.delog(f'不存在{d1}{(MyUtils.listdir(i),f"{ti}_{uid}")}')
        return False
    Maintainace.checkisindisk(videospectrum,func)

# add()
# checkweb()
# delete()
checkisindisk()
# makerecord()
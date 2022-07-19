import os
import shutil
import time

import requests
from selenium.webdriver.common.by import By

import MyUtils

#
# '''
# 需要考虑的压力测试意外特殊情况：
# 多作者、多P
#
# 需要实现的用户需求：
# 能够看到一个用户（通过用户ID检索）看到她发布的全部视频，然后对某个特定视频，能看到这个视频的封面，简介，视频内容，字幕。
#
#
# 组织方式约定：
# E:/Bili/upUID/
#        视频标题BV********.jpg(png)，/BV********/，
#                 分P标题.MP4，简介内容.txt。字幕文件
#
# '''
# # 次生Maintainace
#
# # 先Maintainace'

# t=MyUtils.RefreshTXT(f'D:/Kaleidoscope/bili/CoverSpectrum.txt')
# path='E:/bili/cover/'
# for i in t.l:
#     id=upid(i)
#     print((id,i))
#     if id==None:
#         t.delete(i)
#         t.save()
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


coverspectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/CoverSpectrum.txt')
videouserspectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoUserSpectrum.txt')
path = 'E:/bili/'


def B1():
    # 根据E中的所有后缀重建coverspectrum
    for (root, dirs, files) in os.walk(path):
        lis = dirs
        break
    for dir in lis:
        if not dir.find('_') > 0:
            continue
        coverspectrum.add(dir[dir.rfind('_') + 1:])
        coverspectrum.save()


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


def B2():
    # # 对E盘里的cover进行逐个id筛查是否要并入新的spectrum
    MyUtils.MyDeleteEmpty('./bili/cover')
    for (root, dirs, files) in os.walk('./bili/cover'):
        break
    page = MyUtils.MyChrome(mine=1)
    for dir in dirs:
        page.get(url='https://search.bilibili.com/all?from_source=webtop_search&&keyword=' + dir)
        a = MyUtils.MyElement([page, By.XPATH, '/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/a'], depth=7)
        if a == None:
            continue
        ss = a.get_attribute('href')
        UID = ss[ss.rfind('/') + 1:]
        page.get(f'https://space.bilibili.com/{UID}')
        tt = input()
        if tt.find('e') > 0:
            coverspectrum.add(UID)
            coverspectrum.save()
            if tt.find('f') > 0:
                videouserspectrum.add(UID)
                videouserspectrum.save()
        else:
            MyUtils.MyDeletedir('./bili/cover/' + dir)
    time.sleep(9999)
    page.close()
    MyUtils.MyDeleteEmpty('./bili/cover')


def B3():
    # 清洁spectrum中的重复项
    coverspectrum.save()
    videouserspectrum.save()


def B4():
    #     清洁以前的视频下载
    # 先遍历获得新的标识总集。都包括视频标题
    # 一定是E盘和G盘
    lis1 = []
    lis2 = []
    dlis = []


    def tell(s):
        nonlocal lis1
        for i in lis1:
            if MyUtils.TellStringSame(s, i):
                return True
        return False

    # os.chdir('E:/')
    # for (root,dirs,files)in os.walk('./bili/download'):
    #     break
    # for dir in dirs:
    #     for(a,b,c)in os.walk(f'./bili/download/{dir}'):
    #         break
    #     for bb in b:
    #         for(aa,bbb,cc)in os.walk(a+'/'+bb):
    #             for ccc in cc:
    #                 pp=ccc.strip('.mp4')
    #                 pp=pp[:pp.rfind('-pn')]
    #
    #                 print(ccc)
    #                 if tell(pp):
    #                     dlis.append(os.path.abspath(aa+'/'+ccc))
    # fdlis=MyUtils.RefreshTXT(MyUtils.DesktopPath('dlis.txt'))
    # fdlis.l=dlis
    # fdlis.save()

    # 先删除文件，再删除空文件夹。
    os.chdir('E:/')
    dlis=MyUtils.RefreshTXT(MyUtils.DesktopPath('dlis.txt')).l
    MyUtils.MyDeletedir(dlis)
    MyUtils.MyDeleteEmpty('E:/bili/download')


def B5():
    #     每隔一段时间下载扩充视频库完毕后，遍历仓库
    #     获取更新后的BV号记录、视频标题
    # 这应该是更新BV记录的唯一办法。
    VideoSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoSpectrum.txt')
    title=MyUtils.RefreshTXT('D:/Kaleidoscope/bili/Title.txt')

    lis0=[]
    lis1=[]
    for (root, dirs, files) in os.walk('./bili/'):
        break
    for dir in dirs:
        for (a, b, c) in os.walk(f'./bili/{dir}'):
            break
        for cc in b:
            for(x,y,z)in os.walk(a+'/'+cc):
                break
            name=cc
            bvid = name[name.rfind('_') + 1:]
            if not bvid in lis0 and not bvid in VideoSpectrum.set:
                lis0.append(bvid)
            print(f'[B5] {name} bvid checked.  {VideoSpectrum.length()}')

            for name in z:
                if name.find('.mp4')<0:
                    continue
                if not name in lis1 and not name in title.set:
                    lis1.append(name)
                print(f'[B5] {name} checked.  {title.length()}')
    for i in lis1:
        title.add(i)
    title.save()
    print(f'[B5] 标题记录行为 End。记录{title.length()}条。新增了{len(lis1)}条')
    for i in lis0:
        VideoSpectrum.add(i)
    VideoSpectrum.save()
    print(f'[B5] BV记录行为 End. 记录{VideoSpectrum.length()}条。新增了{len(lis0)}条')


def B6():
    #     对于视频合集，下载器因为是一次性同时解析然后自动下载的，会导致下载时folder视频名字一样。但好在BV名字不一样。
    # 这个函数做的就是找到那些同名upid下的同名视频标题文件夹，查询api，更改视频标题。
    lis = []
    for (root, dirs, files) in os.walk('./bili'):
        for dir in dirs:
            title = []
            for (a, b, c) in os.walk(f'./bili/{dir}'):
                for folder in c:
                    biaoti = folder[:folder.rfind('_')]
                    if not biaoti in title:
                        title.append(biaoti)
                    else:
                        lis.append(os.path.abspath(f'./bili/{dir}/{folder}'))
                break
        break
    print(lis)  # 先检查一下lis对不对


def B7():
    #     通过api，获取所有用户的视频总数，并统计文件夹数目。Print
    sum1 = 0
    sum2 = 0
    UserSpectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoUserSpectrum.txt')

    for UserUID in UserSpectrum.l:
        author = []
        url = (f'https://api.bilibili.com/x/space/arc/search?mid={UserUID}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp')
        res = requests.get(url, headers=MyUtils.headers)
        num = (res.json()['data']['page']['count'])

        #         要通过UID获取ID，决定通过api获得author列表，取众数
        for name in res.json()['data']['list']['author']:
            author.append(name)
        for i in author:
            if author.count(i) >= 0.7 * len(author):
                break
        name = i

        for (root, dirs, files) in os.walk('./bili'):
            break
        for dir in dirs:
            if MyUtils.TellStringSame(dir, name + '_' + UserUID):
                break
        for (root, dirs, files) in os.walk(f'./bili/{dir}'):
            break
        print(f'[MBili B7]{len(dirs)}/{num}')
        sum1 += len(dirs)
        sum2 += num
    print(f'{sum1}/{sum2}')


# B1()
# B2()
# B3()
# B4()
B5()

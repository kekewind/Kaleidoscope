import shutil
import time

import MyUtils
import os
from selenium.webdriver.common.by import By

'''
需要考虑的压力测试意外特殊情况：
多作者、多P

需要实现的用户需求：
能够看到一个用户（通过用户ID检索）看到她发布的全部视频，然后对某个特定视频，能看到这个视频的封面，简介，视频内容，字幕。


组织方式约定：
E:/Bili/upID+upID（曾经用过的所有id序列）+_upUID/
       视频标题BV********.jpg(png)，/BV********/，
                分P标题.MP4，简介内容.txt。字幕文件

'''


# 次生Maintainace

# 先Maintainace'
def upid(UID):
    page = MyUtils.edge(f'https://space.bilibili.com/{UID}')
    title = MyUtils.title([page])
    page.close()
    return title[:title.find('的个人空间')]


# MyUtils.MyDeleteEmpty('./bili/cover')
t = MyUtils.RefreshTXT(f'D:/Kaleidoscope/bili/CoverSpectrum.txt')
# path='E:/bili/cover/'
# for i in count.l:
#     id=upid(i)
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

# 上面是图片转移的代码
# 下面是挨个审查是否要加入扩充coveruser列表
MyUtils.MyDeleteEmpty('./bili/cover/')
for (root, dirs, files) in os.walk('./bili/cover'):
    break
for dir in dirs:
    page = MyUtils.chrome(url='https://search.bilibili.com/all?from_source=webtop_search&&keyword=' + dir, mine=1)
    a = MyUtils.Element([page, By.XPATH, '/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/a'])
    if a == None:
        continue
    ss = a.get_attribute('href')
    UID = ss[ss.rfind('/') + 1:]
    if UID in t.l:
        continue
    page.get(f'https://space.bilibili.com/{UID}')
    tt = input()
    if tt == 'e':
        t.add(UID)
        t.save()
    else:
        MyUtils.deletedirandfile('./bili/cover/' + dir)
    page.close()
time.sleep(9999)

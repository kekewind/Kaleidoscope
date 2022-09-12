import MyUtils
from selenium.webdriver.common.by import By

videouserspectrum=MyUtils.RefreshTXT('D:\Kaleidoscope/bili/VideoUserSpectrum.txt')
videouserexpired=MyUtils.RefreshTXT('D:\Kaleidoscope/bili/VideoUserExpired.txt')
coverspectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/CoverSpectrum.txt')
videouserspectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/VideoUserSpectrum.txt')
downloaded=MyUtils.RefreshTXT('./bili/Downloaded.txt')

#从url中获得useruid
def urltouseruid(c):
    p=['https://space.bilibili.com/',]
    for i in p:
        if i in c:
            c=c[len(i):]
    if c.find('/')>0:
        c=c[:c.find('/')]
    else:
        pass
    return c

# 将用户加入下载列表
def add(uid):
    videouserspectrum.add(urltouseruid(uid))
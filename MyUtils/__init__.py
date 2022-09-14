import datetime
import inspect
import random
import json
import multiprocessing
import os
import re
import shutil
import sys
import time
import urllib3

import pyautogui
import pyperclip
import requests
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


# region
# 复制代码块
# 列表传参法是可行的，只不过最好不要传不是自定义的类
# 如果传参已经是列表就不要再列表传参。直接在函数内使用index。不要在函数内声明，这样会直接创建新的局部变量
# 不建议传递列表进行写。列表本身的大小不能在函数内再改变。字典应该也是同理。
# '//div[starts-with(@style,"transform:")]'
# './div[starts-with(@style,"transform:")]'
#
# endregion
# 注解
# region
def listed(func):
    def inner(*a):
        res=[]
        if type(a[-1])==list:
            b=a[:-1]
            for i in a[-1]:
                res.append(func(*b,i))
            return res
        else:
            return func(*a)
    return inner
# endregion

# 时间
# region

def nowstr():
    return str(datetime.datetime.now())

# 根据完整字符串，返回时间类
def strtotime(s=nowstr()):
    # return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not type(s) == str:
        warn(f'用法错误。s不是字符串而是{info(s)}')
        return
    if len(s) > 10:
        (year, month, day, hour, min) = (
            int(s[0:4]), int(s[s.find('-') + 1:s.rfind('-')]), int(s[s.rfind('-') + 1:s.find(' ')]), int(s[s.rfind(' ') + 1:s.find(':')]),
            int(s[s.find(':') + 1:s.rfind(':')]))
        try:
            mic=int(s[s.find('.') + 1:])
            sec=int(s[s.rfind(':') + 1:s.find('.')])
        except:
            sec=int(s[s.rfind(':') + 1:])
            mic=0
        return datetime.datetime(year, month, day, hour, min, sec, mic)


# 根据完整字符串，返回时间整数
def strtoint(s=nowstr()):
    # return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not type(s) == str:
        warn(f'用法错误。s不是字符串而是{info(s)}')
        return
    if len(s) > 10:
        (year, month, day, hour, min) = (
            int(s[0:4]), int(s[s.find('-') + 1:s.rfind('-')]), int(s[s.rfind('-') + 1:s.find(' ')]), int(s[s.rfind(' ') + 1:s.find(':')]),
            int(s[s.find(':') + 1:s.rfind(':')]))
        try:
            mic=int(s[s.find('.') + 1:])
            sec=int(s[s.rfind(':') + 1:s.find('.')])
        except:
            sec=int(s[s.rfind(':') + 1:])
            mic=0
        return (year, month, day, hour, min, sec, mic)

# 自定义简化时间类
class t():
    def __init__(self,year=0,month=0,day=0,hour=0,min=0,sec=0,mic=0):
        if (year,month,day,hour,min,sec,mic)==(0,0,0,0,0,0,0):
            self.year, self.month, self.day, self.hour, self.min, self.sec, self.mic=strtoint()
            return
        self.year, self.month, self.day=year, month, day
        if not(hour,min,sec)==(0,0,0):
            self.hour, self.min, self.sec=hour,min,sec
        if not(mic==0):
            self.mic==mic

    def s(self):
        return f'{str(self.year).zfill(2)}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:{str(self.min).zfill(2)}:{str(self.sec).zfill(2)}.{str(self.mic).zfill(6)}'

    def counttime(self):
        return counttime(self.s())


# 根据字符串，返回到现在的时间差
def counttime(s):
    return (datetime.datetime.now() - strtotime(s)).total_seconds()
    # if l.find('hms') >= 0:
    #     return time.strftime("%H:%M:%S", time.localtime())
    # if l.find('ms') >= 0:
    #     return time.strftime("%M:%S", time.localtime())
    # if l.find('hm') >= 0:
    #     return time.strftime("%H:%M", time.localtime())
    # if l.find('h') >= 0:
    #     return time.strftime("%H", time.localtime())
    # if l.find('m') >= 0:
    #     return time.strftime("%M", time.localtime())
    # if l.find('l') >= 0:
    #     return time.strftime("%S", time.localtime())
    # if l=='all':
    #     return str(datetime.datetime.nowstr())


def timestamp():
    # 返回数字
    return time.time()


# endregion

# 调试模式
# region


def Debug():
    global debug
    debug = True


def Run():
    global debug
    debug = False

def retry(e):
    log(f'{type(e)}错误，重建中 ...')
    if type(e) in retrylist:
        return True
    return  False

# endregion

# 特殊功能函数
# region
def Input(x, y, s):
    # 在屏幕指定位置进行剪贴板复制粘贴并按下回车
    pyperclip.copy(s)
    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.hotkey('ctrl' + 'v')
    time.sleep(0.5)
    pyautogui.hotkey('Enter')
    time.sleep(1)


def TellStringSame(s1, s2, ratio=1):
    s1 = str(s1)
    s2 = str(s2)
    if len(s1) > 3 and len(s2) > 3:
        if s1.rfind(s2) >= 0 or s2.rfind(s1) >= 0:
            return True
    if len(s1) / len(s2) < ratio / 2 or len(s2) / len(s1) < ratio / 2:
        return False

    if len(s1) > 5:
        for i in range(max(int(len(s1) * (1 - ratio)), 1)):
            if s1[i:min(len(s1), i + int(len(s1) * ratio))] in s2:
                return True
    if len(s2) > 5:
        for i in range(max(int(len(s1) * (1 - ratio)), 1)):
            if s2[i:min(len(s2), i + int(len(s2) * ratio))] in s1:
                return True
    return False


def tellstringsame(s1, s2):
    # 只对中文开放
    return TellStringSame(s1, s2)


def cutvideo(inputpath, outputpath, start, end):
    # 使用ffmpeg剪切视频
    sourcepath = os.path.abspath(inputpath)
    command = f'ffmpeg  -i {inputpath} -vcodec copy -acodec copy -ss {start} -to {end} {outputpath} -y'
    os.system('"%s"' % command)

@listed
def info(s):
    # 综合返回磁盘空间、文件夹或者文件信息、变量大小和类型
    # 类型错误
    if type(s) in [int, ]:
        warn(f'用法错误。传入参数为{type(s)}类型')
        return
    # 磁盘
    if len(s) == 1 and type(s) == str:
        gb = 1024 ** 3  # GB == gigabyte
        try:
            total_b, used_b, free_b = shutil.disk_usage(s.strip('\n') + ':')  # 查看磁盘的使用情况
        except Exception as e:
            warn(e)
            return 0
        # log('总的磁盘空间: {:6.2f} GB '.format(total_b / gb))
        # log('已经使用的 : {:6.2f} GB '.format(used_b / gb))
        # log('未使用的 : {:6.2f} GB '.format(free_b / gb))
        return (free_b / gb)
    # 文件
    if type(s) != str or type(s) == str and not os.path.exists(s[:224]):
        try:
            tip(f'类型：{type(s)} 大小：{int(int(sys.getsizeof(s) / 1024 / 1024 * 100) / 100.0)}MB 内存地址：{id(s)} 长度{len(list(s))}')
        except Exception as e:
            warn(e)
            tip(f'类型：{type(s)} 大小：{int(int(sys.getsizeof(s) / 1024 / 1024 * 100) / 100.0)}MB 内存地址：{id(s)}')
            return '用法错误。可能是调用了print(provisional.info)导致的。'
        return
    s = str(s)
    if s == '':
        warn(f'用法错误。s或许应为字符串而不是s={s}')
    path = standarlizedPath(s)
    if os.path.exists(path):
        if not path.rfind('.') > 1:
            ()


# endregion

# 进程池与线程池
# region
# endregion

# 爬虫
# region
def alertpage(l):
    page=l[0]
    page.switch_to.window(page.window_handles[0])

def Element(l, depth=5, silent=None):
    res = elements(l, depth, silent)
    if res == []:
        return None
    else:
        return res[0]


def elements(l, depth=5, silent=None):
    return Elements(l, depth, silent)


def Elements(l, depth=5, silent=None):
    """
    返回元素列表，找不到为[]
    :param l:
    :return:
    """
    page = l[0]
    method = l[1]
    s = l[2]
    result = page.find_elements(method, s)
    # delog((page,method,s))
    # delog((result,type(result),len(result)))
    if len(result):
        return result
    else:
        depth += 1
        time.sleep(2)
        if debug and not silent:
            tip(f'元素未找到，重试... method={method}, string={s}')
        if depth >= 10:
            if not silent:
                warn(f'最终未获取到元素。 method={method},str={s}')
            return []
        else:
            return Elements(l, depth, silent)

# 必须要跳过的
def skip(l,strict=False):
    """
    简单跳过，不做操作，等待人工操作来跳过，否则一直等待
    :param l:列表：页面，XPATH/ID，字符串
    :return:
    """
    page = l[0]
    method = l[1]
    s = l[2]
    time.sleep(1)
    if Element([page, method, s], depth=8, silent=True):
        warn(f'{s} detected. 等待其消失中以继续。。。')
        alertpage([page])
        # if strict==True:
        #     log(f'严格模式已打开。准备重建...')
        #     raise retrylist[0]
        WebDriverWait(page, 9999, 3).until_not(expected_conditions.presence_of_element_located(locator=(method, s)))
        time.sleep(2)

def getscrolltop(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollTop;return(q)')


def scrollheight(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollHeight;return(q)')


def scroll(l, silent=None):
    """

    :param l: 页面，第二个参数小于1可不传
    :return:
    """
    log('滚动中..')
    ti = time.time()
    page = l[0]
    ratio = 1
    if len(l) > 1:
        ratio = l[1]
    ScrollTop = -1
    while ScrollTop != getscrolltop([page]):
        ScrollTop = getscrolltop([page])
        if not silent == None:
            delog(ScrollTop)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != getscrolltop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != getscrolltop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != getscrolltop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != getscrolltop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(3)
        if ScrollTop != getscrolltop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
    log(f'滚动完毕。 {time.time() - ti} s.')


def requestdownload(LocalPath, mode, url):
    CreatePath(LocalPath)
    try:
        with open(LocalPath, mode) as f:
            f.write(requests.get(url=url, headers=headers).content)
    except(requests.exceptions.SSLError):
        try:
            with open(LocalPath, mode) as f:
                f.write(requests.get(url=url, headers=headers, verify=False).content)
        finally:
            input('SSLError')
            requestdownload(LocalPath, mode, url)


def chrome(url='', mine=None, silent=None, t=100):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maxmized')
        if not mine == None:
            time.sleep(3)
            options.add_argument(f"--user-data-dir=C:\\Users\\17371\\AppData\\Local\\Google\\Chrome\\User Data")
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
        if not silent == None:
            options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        # driver.maximize_window()
        driver.set_page_load_timeout(t)
        driver.set_script_timeout(t)
        if not url == '':
            driver.get(url)
        return driver
    except selenium.common.exceptions.InvalidArgumentException:
        driver.quit()
        warn('旧页面未关闭。请关闭。')
        c=input()
        return chrome()


class Edge():
    def __init__(self, url='', silent=None):
        self.driver = edge(url=url, silent=silent)

    def click(self, s):
        return click([self.driver, By.XPATH, s])

    def element(self, s):
        return Element([self.driver, By.XPATH, s])

    def elements(self, s):
        return Elements([self.driver, By.XPATH, s])

    def scroll(self):
        scroll([self.driver])

    def __del__(self):
        self.driver.quit()

    def open(self,url):
        url='https://'+url.strip('https://')
        self.driver.execute_script(f"window.open('{url}')")
        self.switchto()

    def get(self,url):
        url='https://'+url.strip('https://')
        self.driver.get(url)

    def switchto(self,n=-1):
        self.driver.switch_to.window(self.driver.window_handles[n])

class Chrome(Edge):
    def __init__(self, url='', mine=None, silent=None, time=100):
        self.driver = chrome(url, mine=mine, silent=silent, time=time)


def edge(url='', silent=None):
    options = webdriver.EdgeOptions()
    if not silent == None:
        options.add_argument('headless')
    try:
        driver = webdriver.Edge(options=options)
    except selenium.common.exceptions.SessionNotCreatedException:
        warn('貌似msedgedriver.exe版本过低。已经自动复制网址链接。请打开浏览器进行下载。')
        pyperclip.copy('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
        delog('点击 edge://version/ 以查看浏览器版本。')
        sys.exit(-1)
    finally:
        ()
    if not url == '':
        driver.get(url)
    return driver


def click(l):
    if len(l) > 2:
        try:
            Element(l).click()
            return
        except:
            try:
                ActionChains(l[0]).move_to_element(to_element=Element(l)).click().perform()
                return
            except Exception as e:
                warn(['click error！', e])
    else:
        page = l[0]
        element = l[1]
        try:
            element.click()
            return
        except:
            try:
                ActionChains(page).move_to_element(to_element=element).click().perform()
                return
            except Exception as e:
                warn(['click error!', e])

    time.sleep(1)


def MyPress(l):
    page = l[0]
    s = l[1]
    if s == 'down':
        k = Keys.DOWN
    ActionChains(page).key_down(k).key_up(k).perform()


def MyTitle(l):
    page = l[0]
    element = Element([page, By.XPATH, '/html/head/title'])
    if element == None:
        return None
    return standarlizedFile(element.get_attribute('text'))


def setscrolltop(l):
    (page, x) = l
    page.execute_script(f'document.documentElement.scrollTop={x}')


def pagedownload(url, path, t=15, silent=True, depth=0, auto=None):
    # 如果下载失败，再下载一次
    def recursive():
        time.sleep(t)
        page.quit()
        time.sleep(1)
        if os.path.exists(path + '.crdownload'):
            os.remove(path + '.crdownload')
            warn(f'{t}s后下载失败。没有缓存文件存留（自动删除） 请手动尝试 {url}')
            # warn(f'download failed.No crdownload file left(auto deleted). you may try{url}')
            return pagedownload(url, path, t=t + t, depth=depth + 1)
        return True

    # 递归停止条件
    # region
    if depth > 5:
        warn('最终下载失败。没有缓存文件存留（自动删除） 请手动尝试 {url}')
        return False
    # endregion

    # 获取变量
    # region
    path = standarlizedPath(path,strict=True)
    if path.find('.') < 0:
        path += '/'
    root = (path[:path.rfind('\\')])
    name = path[path.rfind('\\') + 1:]
    options = webdriver.ChromeOptions()
    # 设置下载路径
    prefs = {'download.default_directory': f'{root}'}
    options.add_experimental_option('prefs', prefs)
    if silent == True:
        options.headless = True
    page = webdriver.Chrome(chrome_options=options)
    # endregion

    # 打开页面
    try:
        page.get(url)
        # 如果服务器直接403
        # region
        if tellstringsame(page.title, '403 forbidden'):
            warn(f'这个url已经被服务器关闭  403  ：{url}')
            return False
        # endregion

    except Exception as e:
        # 仍然可以强制下载的报错
        if type(e) in [ZeroDivisionError, ]:
            warn(e)
        elif type(e) in [selenium.common.exceptions.WebDriverException]:
            # 需要重启pagedownload的下载报错
            warn(e)
            page.quit()
            return pagedownload(url, path, t, silent, depth + 1)
        else:
            warn(e)
            warn(type(e))
            sys.exit(-1)

    i = 0
    # 如果这个链接打开就能自动下载
    # region
    if not auto == None:
        return recursive()
    # endregion

    # region
    while i < 10:
        # 什么？？？竟然要尝试10次，哈哈哈真是笑死我了
        try:
            page.execute_script(f"var a1=document.createElement('a');\
            a1.href='{url}';\
            a1.download='{name}';\
            console.log(a1);\
            a1.click();")
            break
        except:
            warn('下载重试中...')
            i += 1
    # endregion

    return recursive()


def scrshot(l):
    (element, path) = l
    path = standarlizedPath(path)
    path = path.strip('.png') + '.png'
    file('wb', path, element.screenshot_as_png)


# endregion

# 文件读写
# region
# 重命名
def rename(s1,s2):
    os.rename(standarlizedPath(s1),standarlizedPath(s2))

# 判断文件
def isfile(s):
    s=standarlizedPath(s)
    if os.path.exists(s):
        if None==listfile(s) and None==listdir(s):
            return True
    return False

# 判断文件夹
def isdir(s):
    s=standarlizedPath(s)
    if os.path.exists(s):
        if list==type(listfile(s)):
            return True
    return False

# 复制文件夹
def copydir(s1,s2):
    s1,s2=standarlizedPath(s1),standarlizedPath(s2)
    s1,s2= pathname(s1), pathname(s2)
    shutil.copy(s1,s2)

# 复制文件
def copyfile(s1,s2):
    s1,s2=filename(s1,s2)
    shutil.copy(s1,s2)

# 移动
def move(s1,s2):
    shutil.move(standarlizedPath(s1),standarlizedPath(s2))

def listdir(path):
    path = standarlizedPath(path)
    for (root, dirs, files) in os.walk(path):
        ret = dirs
        for i in ['$RECYCLE.BIN', 'System Volume Information']:
            try:
                ret.remove(i)
            except:
                pass
        # delog(str(ret))
        ret1 = []
        for i in ret:
            ret1.append(standarlizedPath(root + '/' + i))
        return ret1

@listed
def listfile(path):
    path = standarlizedPath(path)
    for (root, dirs, files) in os.walk(path):
        ret = files
        for i in ['DumpStack.log', 'DumpStack.log.tmp', 'pagefile.sys']:
            try:
                ret.remove(i)
            except:
                pass
        ret1 = []
        for i in ret:
            ret1.append(standarlizedPath(root + '/' + i))
        # delog(str(ret))
        return ret1


# 直接返回路径的文件夹路径
def pathname(s=None):
    s = standarlizedPath(s)
    return s[:s.rfind('/') + 1]

# 返回文路径的文件名
def filename(s):
    s = standarlizedPath(s)
    s= s[s.rfind('/') + 1:]
    if s=='':
        warn('空')
        sys.exit(-1)
    return standarlizedFile(s)


class csv():
    def __init__(self, path):
        self.path = standarlizedPath(path)
        self.f = open(self.path)
        self.reader = csv.reader(self.f)
        self.header = next(self.reader)

    def get(self, begin, end):
        count = 0
        res = []
        for row in self.reader:
            if count < begin:
                continue
            if count >= end:
                break
            res.append(row)
        return res



def deletedirandfile(l, silent=None):
    # 递归删除dir_path目标文件夹下所有文件，以及各级子文件夹下文件，保留各级空文件夹
    # (支持文件，文件夹不存在不报错)
    def del_files(dir_path):
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path)  # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                if silent == None:
                    print(e)
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                # if file_name != 'wibot.log':
                tf = os.path.join(dir_path, file_name)
                del_files(tf)
        if silent == None:
            log(dir_path + '  removed.')

    if not type(l) == list:
        l = [l]
    # e = MyThreadPool(1000)
    for file in l:
        # e.excute(del_files,file)
        del_files(file)
    for i in l:
        if os.path.exists(i):
            shutil.rmtree(i)


# 统一路径格式
def standarlizedPath(s='',strict=False):
    b=False
    if s == '':
        s = __file__
    if s[-1]in ['/','\\']:
        b=True
    try:
        s = os.path.abspath(s)
    except Exception as e:
        warn(e)
        sys.exit(-1)
    if b:
        s+='/'
    if strict:
        return s.replace('/', '\\')
    return s.replace('\\', '/')


# 合法化文件名
def standarlizedFile(str):

    str = re.sub('/|\||\?|>|<|:|\n|/|"|\*', ' ', str)
    str = str.replace('  ', ' ')
    str = str.replace('\\', ' ')
    str = str.replace('\r', ' ')
    str = str.replace('\t', ' ')
    str = str.replace('\x08', ' ')
    str = str.replace('\x1c', ' ')

    return str[:224]


def CreatePath(path):
    """
    只创建空文件夹
    :param path: ’\‘自动转换为‘/’
    :return:成功或者已存在返回路径字符串，否则返回False
    """
    path = pathname(path)
    # if not path.rfind('.') > 1:
    #     path = path + '/'
    if os.path.exists(path):
        return path
    try:
        os.makedirs(path)
        return path
    except Exception as e:
        warn(e)
        warn(f'Create {path} Failed.')
        sys.exit(-1)


def createpath(path):
    return CreatePath(path)


def createfile(path, encoding=None):
    # 文件已存在返回False，成功返回True
    path = standarlizedPath(path)
    root = pathname(path)
    createpath(path)
    name = standarlizedFile(path[path.rfind('/') + 1:])
    if not path == root + name:
        tip(f'文件名{path}不规范，已重命名为{root + name}')
    path = root + name
    if os.path.exists(path):
        warn(f'{path} alreay exists. 文件已存在')
        return False
    # try:
    if not encoding == None:
        with open(path, 'w') as f:
            ()
    else:
        with open(path, 'wb', encoding=encoding) as f:
            ()
    # except Exception:
    #     warn(f'创建文件{path}未知失败。{str(Exception)}')
    #     return False
    return True


def file(mode, path, IOList=None, encoding=None):
    # 所有文件with open的封装
    try:
        path = standarlizedPath(path)
        createpath(path)
        if (IOList == None or IOList == []) and (mode.find('w') > -1 or mode.find('a') > -1):
            warn(f'可能是运行时错误。写未传参。IOList: {info(IOList)} mode: {mode}')
            sys.exit(-1)
        if not os.path.exists(path) and mode.find('r') > -1:
            warn(f'错误。读不存在文件：{path}')
            return False
        # 比特流
        if mode == 'rb':
            with open(path, mode='rb') as file:
                return extend(IOList, file.readlines())
        # 字符流
        elif mode == 'r':
            with open(path, mode='r', encoding=encoding) as file:
                return extend(IOList, file.readlines())
        elif mode == 'w':
            with open(path, mode='w', encoding=encoding) as file:
                file.writelines(IOList)
        elif mode == 'wb':
            try:
                with open(path, mode='wb') as file:
                    file.write(IOList)
            except:
                with open(path, mode='wb') as file:
                    file.writelines(IOList)
        elif mode == 'a':
            with open(path, mode='a', encoding=encoding) as file:
                file.writelines(IOList)
    except Exception as e:
        warn(e)
        warn(info(IOList))
        sys.exit(-1)


def DesktopPath(s=''):
    if s=='new':
        s=random.randint(0,99999)
        s=str(s)
        log(f'桌面新建：{s}')
    return 'C:/Users/17371/Desktop/' + s


def desktoppath(s=''):
    return DesktopPath(s)

def desktop(s=''):
    return DesktopPath(s)

class txt():
    def __init__(self, path, encoding='utf-8'):
        if encoding == None:
            encoding = 'utf-8'
        self.encoding = encoding
        self.path = standarlizedPath(path)
        if not self.path.find('.') > 0:
            self.path += '.txt'
        self.l = []
        if not os.path.exists(self.path):
            createfile(self.path, encoding=encoding)
            return
        for i in file('r', self.path, IOList=[], encoding=encoding):
            self.l.append(str(i).strip('\n'))

    @listed
    def add(self, i):
        self.l.append(str(i))
        file('a', self.path, [str(i)], encoding='utf-8')

    def save(self):
        # 强制写
        slist = []
        for i in self.l:
            slist.append(i + '\n')
        if slist == []:
            slist = ['']
        file('w', self.path, slist, encoding=self.encoding)
        warn(f'saved -  {tail(self.path, "/")}')

    def length(self):
        return len(self.l)

    def clear(self):
        self.l = []
        self.save()


class RefreshTXT(txt):
    # 实现逐行的记录仓库
    # 实现备份
    # 增删都会执行保存操作。
    def __init__(self, path, encoding=None):
        txt.__init__(self, path, encoding)
        self.loopcount = 0
        # self.rollback()
        self.set()
        self.backup()

    def backup(self):
        # 备份
        # region
        backupname = self.path.strip('.txt') + '_backup.txt'
        if not os.path.exists(backupname):
            f = txt(backupname, self.encoding)
            extend(f.l, extend([nowstr()], self.l))
            f.save()
        else:
            if counttime(txt(backupname).l[0]) > 3600 * 24:
                f = txt(backupname)
                f.l = extend([nowstr()], self.l)
                f.save()
        # endregion

    def set(self):
        #         去重，去空，集合化
        # region
        p = list(set(self.l))
        p.sort(key=self.l.index)
        self.l = p
        if '' in self.l:
            self.l.pop(self.l.index(''))
        txt.save(self)

    def save(self):
        RefreshTXT.set(self)
        txt.save(self)

    def rollback(self):
        if len(self.l) < 1:
            return None
        self.l = extend(self.l[1:], [self.l[0]])
        self.loopcount -= 1
        self.save()
        warn('rollbacked.')
        return self.l[-1]

    def get(self):
        txt.__init__(self, self.path, self.encoding)
        if len(self.l) <= 1:
            return None
        self.l = extend([self.l[-1]], self.l[:-1])
        self.loopcount += 1
        self.save()
        return self.l[0]

    def delete(self, l):
        b = False
        if type(l) == list:
            for i in l:
                j = dicttojson(i)
                if j in self.l:
                    self.l.pop(self.l.index(j))
                    warn(f'删除{j}在{self.path}中')
                    b = True
            if not b:
                warn(f'尝试删除但是记录{self.path}中没有以下列表中的任何一个元素 {l}.')
            RefreshTXT.save(self)
        else:
            RefreshTXT.delete(self, [l])

    @listed
    def add(self, i):
        i=str(i)
        if not i in self.l:
            txt.add(self, '\n'+i)


class Json(txt):
    def __init__(self, path, encoding=None):
        txt.__init__(self, path, encoding)
        self.addtodict()

    def addtodict(self):
        self.d = {}
        for i in self.l:
            if i=='':
                continue
            try:
                self.d.update(jsontodict(i))
            except:
                warn(self.path)
                warn(f'-{i}-')
                print(type(i))
                print(info(i))
                sys.exit(-1)

    def add(self, d):
        txt.add(self, dicttojson(d)+'\n')
        self.d.update(jsontodict(d))

class RefreshJson(Json, RefreshTXT):
    def __init__(self, path):
        RefreshTXT.__init__(self, path)
        Json.addtodict(self)

    def get(self):
        return jsontodict(RefreshTXT.get(self))

    def rollback(self):
        return jsontodict(RefreshTXT.rollback(self))

    @listed
    def add(self, i):
        for j in self.l:
            if '' in self.l:
                nn=self.l.index('')
                warn(f'检测到RefreshJson{self.path}的第{nn}行有空字符记录，已停止程序。上下行：{self.l[nn-1],self.l[nn],self.l[nn+1]}')
                sys.exit()
            if list(jsontodict(i).keys())[0] == list(jsontodict(j).keys())[0]:
                self.delete(j)
                break
        self.d.update(jsontodict(i))
        RefreshTXT.add(self, dicttojson(i))

    def delete(self, i):
            RefreshTXT.delete(self, dicttojson(i))
            if list(jsontodict(i).keys())[0] in self.d:
                self.d.pop(list(jsontodict(i).keys())[0])
            else:
                warn(f'{list(jsontodict(i).keys())[0]}不在{self.path}中。')


class cache():
    def __init__(self, path):
        self.path = path

    def get(self):
        while True:
            try:
                f = txt(self.path)
                if f.l == []:
                    return None
                s = jsontodict(f.l[0])
                f.l.pop(0)
                f.save()
                return s
            except Exception as e:
                warn(e)
                warn('cache获取失败。正在重试')
                time.sleep(2)

    def add(self, s):
        s = dicttojson(s)
        f = txt(self.path)
        f.add(s)
        f.save()

    def length(self):
        return txt(self.path).length()

class rtxt(RefreshTXT):
    pass
class rjson(RefreshJson):
    pass

# endregion

# 日志
# region
def Log(s, x1, x2, x3=7 , x4=30,x5=30):
    s = str(s)
    try:
        pp1 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[2]
        pp2 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[0]
        pp3 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[1]
        pp1 = f'[{pp1}]'
        pp2 = pp2[len(pathname(pp2)):]
    except:
        pp1 = None
    try:
        pp4 = inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back)[2]
        pp5 = inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back)[0]
        pp6 = inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back)[1]
        pp4 = f'[{pp4}]'
        pp5 = pp5[len(pathname(pp5)):]
    except:
        pp4 = None
        pp5 = None
        pp6 = None
    s2 = f'\033[{x3};{x4}m'
    for i in range(len(pp2) // 4 - 7):
        s2 += '\t'
    s2 += f'{s}'
    for i in range(17 - len(s2) // 4 + 3):
        s2 += '\t'
    s2 += '\033[0m'
    global Logcount
    print(
        f'[{Logcount}] \033[7;{x5}m  {str(strtotime(nowstr()).hour).zfill(2)}:{str(strtotime(nowstr()).minute).zfill(2)}:{str(strtotime(nowstr()).second).zfill(2)} \033[{x1};{x2}m {pp4} {pp5}  <line {pp6}> ==》 {pp1} {pp2}  <line {pp3}> \033[0m' + s2)
    Logcount += 1

@listed
def log(s):
    Log(s, 7, 32)

@listed
def tip(s):
    Log(s, 7, 34, 9, 35)

@listed
def delog(s=0):
    if not debug:
        return
    if s == 0:
        delog('is Processing.')
        return
    if s == -1:
        # 手动打终点断点，所以会退出
        delog('Processed.')
        sys.exit(0)
        return
    dic = {'begin': 'Announce Begin',
           'end': "Announce End",
           'a': 'Announce Begin',
           'z': "Announce End"
           }
    try:
        if str(s) in dic.keys():
            s = dic.get(s)
    finally:
        Log(s, 7, 34)


def warn(s):
    Log(s, 7, 31)


# endregion

# 基础数据结构
# region
def extend(l1, l2):
    if l1 == None:
        warn(f'l1: None  l2: {l2}')
        return l2
    for i in l2:
        l1.append(i)
    return l1

class MyError(BaseException):
    pass

def jsontodict(s):
    if type(s) == dict:
        return s
    if s == '' or s == None:
        warn(f'{s,type(s)}')
        return
    try:
        return json.loads(s)
    except Exception as e1:
        warn([s, e1])
        sys.exit(-1)


def dicttojson(s):
    if type(s) == str:
        return s
    try:
        return json.dumps(s, ensure_ascii=False)
        # return str(s)
    except Exception as e:
        warn(e)
        return ''

def keys(d):
    if not type(d)==dict:
        warn(f'用法错误。d的类型为{type(d)}')
    return list(d.keys())

def dicttolist(d):
    return keys(d)

# endregion
# 字符串
# region
def tail(s, mark):
    s, mark = str(s), str(mark)
    return s[s.rfind(mark) + len(mark):]


def strre(s, pattern):
    return (re.compile(pattern).findall(s))


# endregion


# 分布式
# region

#   更改工作目录
def setRootPath():
    for i in activedisk.l:
        if info(i) >= 0.2:
            os.chdir(i + ':/')
            log(f'operating DISK {str.title(i)}')
            break


#     初始化一个分布式盘
def initdisk(diskname):
    if not diskinfo.l == []:
        warn(f'初始化分布盘失败。当前盘{standarlizedPath("./")}已存在diskInfo.txt。请检查。')
        return False
    if diskname in disknames.l:
        warn(f'该名字已存在。请更换。')
        return getdiskname()
    diskinfo.add({"name": str(diskname)})
    disknames.add(diskname)
    return


# 与操作盘diskinfo交互
def getdiskname():
    if not os.path.exists('./diskInfo.txt') or diskinfo.l == []:
        name = input(f'检测到当前操作盘未初始化。请输入盘符（后期沿用，慎重！）：\n\t\t\t\t（已启用的唯一名）{RefreshTXT("D:/Kaleidoscope/disknames.txt").l}')
        initdisk(name)
    else:
        disknames.add(diskinfo.d['name'])
    return diskinfo.d['name']


# endregion




# __init__()
# region
debug = True
headers = {
    'user-agent': '\
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36\
                  ',
    'cookie': \
        'douyin.com; __ac_referer=__ac_blank; ttcid=431befd8b5104ec2b3e9935bc6ec52f617; s_v_web_id=verify_l17s6pii_nh6oZDhq_iYxA_4ytu_ANgk_OTyTTCcg2xKS; douyin.com; csrf_session_id=6773d2a77c2678be09d4643511e64a6b; passport_csrf_token=ec7dfe616ded3178be26b33769703ec3; passport_csrf_token_default=ec7dfe616ded3178be26b33769703ec3; live_can_add_dy_2_desktop=%221%22; download_guide=%223%2F20220806%22; THEME_STAY_TIME=%22299980%22; IS_HIDE_THEME_CHANGE=%221%22; __ac_nonce=062f0b4060092bc3a4977; __ac_signature=_02B4Z6wo00f01hCbMoQAAIDCkJnIxJqXz.oQuzYAAObkIAmDFqT5eYtXQLOIndt3rqBiTrG-CP3fU3NbcCEhFtr9r1pPKbWfEluNFR83rgs19EQFlu6MM54rVDDiMOkZpWeEUrxin.D9jwp.fd; strategyABtestKey=1659941895.313; home_can_add_dy_2_desktop=%221%22; tt_scid=g3OvOz0oZqKoRGifS-F3fVy9Uku8K1fcPIo.H58wX9ckfCVHoYw0ftRBmQUwpdW28229; msToken=DyrYcuwheFZCpvBdU_rl7x872ZpxcFUjmoUmnVSUjv5iH-OY4kfwy6vn4VvEVHnixrP6nJw59CWQmCznZwzJJI1-Ux37b8ACpJ7F4-8Jb8J4vxHPP-rGW6yTQZs=; msToken=wiua9ZhBny4jw_muW9lEdGu6MpWNaAGgpTSDW6NqhoScfcwHrJ-0onvVi7sOuh5o9bR19EbBW8BBTEhVpGsEsbKCYGmYIL6zJJglE8Gr4FBqa2PREXaSkNNgwv8=' \
    }
root=standarlizedPath(__file__)
root=root[:root.rfind('/')]
root=root[:root.rfind('/')]+'/'
Logcount = 0
activedisk = txt('D:/Kaleidoscope/ActiveDisc.txt')
disknames = RefreshTXT("D:/Kaleidoscope/disknames.txt")
setRootPath()
diskinfo = RefreshJson('./diskInfo.txt')
diskname = getdiskname()
retrylist=[selenium.common.exceptions.WebDriverException,MyError,selenium.common.exceptions.ElementClickInterceptedException,Exception,ConnectionRefusedError,urllib3.exceptions.NewConnectionError,urllib3.exceptions.MaxRetryError]
tip('MyUtils already loaded')
# endregion

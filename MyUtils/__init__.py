import _thread
import os
import re
import sys
import shutil
import time
import inspect


from concurrent.futures import ThreadPoolExecutor

import cv2
import prompt_toolkit.clipboard.pyperclip
import prompt_toolkit.clipboard.pyperclip
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
import Levenshtein
from PIL import Image

# '//div[starts-with(@style,"transform:")]'
import MyUtils

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34',
    'cookie': 'douyin.com; ttcid=431befd8b5104ec2b3e9935bc6ec52f617; ttwid=1%7CBKDk4yeaBU1MV1-fraGgP1L1JdWPpe8YdQAQJ7zvkoc%7C1638280535%7C0de0bc257260629cad68f3e48827aa87dee824843719de85d6df5740b98a0b35; MONITOR_WEB_ID=61cd5100-8922-4e27-a39e-cff1aac97744; passport_csrf_token_default=8808f41976c316e1e4feeccc71659214; passport_csrf_token=8808f41976c316e1e4feeccc71659214; _tea_utm_cache_6383=undefined; s_v_web_id=verify_kyl03m2t_DbovL5hY_XEdE_4D3F_8ydf_SRFUbtcXvvzx; odin_tt=8c8649b73924e20b8ebd0865fe23dfff20abaa1c55057cc47a9e8995db9a8864b4068c42788c57d1bf943304c820a3a2265b74893008430f9b8ac37b9ffb30d8; MONITOR_DEVICE_ID=c7204e31-c2a3-4dda-9f7a-1b8411427356; douyin.com; _tea_utm_cache_1300=undefined; THEME_STAY_TIME=299336; IS_HIDE_THEME_CHANGE=1; pwa_guide_count=3; AB_LOGIN_GUIDE_TIMESTAMP=1642679265520; msToken=4_7ivDwiz55j5pmRF7atvbaf8SgF0y-eI27hDQZdBLq1YopXPbpC0w6sEDpLwKT00_5TzheRLUQ2sglBwgjWIqgnBHEXvP6eaUjNTXAiI2u1zwcdmTYHPDn8; __ac_nonce=061e95f77000bfa192695; __ac_signature=_02B4Z6wo00f01-ieBLAAAIDDaJz-8r8-h7fougAAAJvYGPJCHKcJjZKArtIgyqihOTmvd-8l-caB2p5EGf2-stiZBGEHYZi7rSyMXHQ8WZLWSz5p9AZQBzyIJN8ePDZ-bHh8Om-ryvd9bgnDf9; home_can_add_dy_2_desktop=1; tt_scid=W7mNcA0UmM9ddpdpKWW5LuB65BLEdJNsmETvz8y2qVv7kJQ14Ipb3-YDhjLfk-g54cc0; msToken=0rskkPniKM-M-1bVn67L-VEt7ef70JcEzqvxTNS7XYW_oDlImtGCB_V2XXJ_zpCB3SdaLFPMntJc711qeys6npV4YkXXCWI-ttAjdZgerI9XGkCdmgGv264='
}
Root = __file__
Root = Root[0:Root.rfind('/')]
hashRoot = 'D:/Programme Files/Spectrum'


def MyDeletedir(l,silent=None):
    # 递归删除dir_path目标文件夹下所有文件，以及各级子文件夹下文件，保留各级空文件夹
    # (支持文件，文件夹不存在不报错)
    def del_files(dir_path):
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path)  # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                print(e)
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                # if file_name != 'wibot.log':
                tf = os.path.join(dir_path, file_name)
                del_files(tf)
        if silent==None:
            print(dir_path + '  removed.')

    if not type(l)==list:
        l=[l]
    e=MyPool(1000)
    for file in l:
        # e.excute(del_files,file)
        del_files(file)


def MyGetPath():
    s = __file__
    s = s[:s.rfind('\\')]
    return s


def MyCreatePath(path):
    """
    只创建文件夹
    :param path: ’\‘自动转换为‘/’
    :return: 不返回值
    """
    if not path.rfind('.') > 1:
        path = path + '/'
    while path.rfind('//') > 0:
        path = re.sub('//', '/', path)
    if path.rfind('/') > 0:
        path = path[0:path.rfind('/')]
    else:
        path = path[0:path.rfind('\\')]
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print(f'Create path Failed. {path}')


def MyFile(mode, path, IOList=[]):
    """
    读内容不需要第三参数，写内容传入列表，
    不要去掉\n，这样反而还会影响重新写入所需要的\n
    :param mode: 'w'或'r'等
    :param path:
    :param IOList: 写入的列表内容
    :return:
    """
    MyCreatePath(path)
    if mode == 'rb':
        with open(path, mode='rb') as file:
            if IOList == []:
                return (file.readlines())
            else:
                IOList = file.readlines()
                return
    elif mode == 'r':
        if not IOList == []:
            with open(path, mode='r', encoding='utf-8') as file:
                IOList = file.readlines()
                return
        if not os.path.exists(path):
            MyFile('w', path, [])
            return []
        with open(path, mode='r', encoding='utf-8') as file:
            return (file.readlines())
    elif mode == 'rs':
        if not os.path.exists(path):
            MyFile('w', path, [])
            return []
        with open(path, mode='r', encoding='utf-8') as file:
            content = file.readlines()
            newset = list(set(content))
            newset.sort(key=content.index)
            MyFile('w', path, newset)
            if not IOList == []:
                IOList = newset
                return
            return newset
    elif mode == 'w':
        with open(path, mode='w', encoding='utf-8') as file:
            file.writelines(IOList)
    elif mode == 'wb':
        try:
            with open(path, mode='wb') as file:
                file.write(IOList)
        except:
            with open(path, mode='wb') as file:
                file.writelines(IOList)


def MyVerifyPic(l):
    page = l[0]
    id = l[1]
    if not expected_conditions.presence_of_element_located(locator=(By.ID, id)):
        return
    deltax = 0
    elemenrt = page.find_element_by_id(id)
    ActionChains(page).move_to_element(elemenrt).perform()

    def get_pos(image):
        blurred = cv2.GaussianBlur(image, (5, 5), 0, 0)
        # Canny
        # edges = cv2.Canny(image, threshold1,threshold2, apertureSize, L2gradient)
        # threshold1计算过程中使用的第一个阈值，通常为最小阈值
        # threshold2计算过程中使用的第二个阈值，通常为最大阈值
        # apertureSize 可选参数，Sobel算子的孔径大小
        # L2gradient 可选参数，计算图像梯度的标识，默认值为False，值为True时会采用更精确的方法计算。
        canny = cv2.Canny(blurred, 200, 400)
        # contours, hierarch = cv2.findCours(image, mode, methode)
        # cv2.RETR_EXTERNAL只检测外轮廓
        # cv2.CHAIN_APPROX_SIMPLE只保存水平，垂直或对角线轮廓的端点
        # contours 检测出所有的轮廓，列表类型，每一个元素都是某个轮廓的像素坐标数组
        # hierarchy 轮廓之间的层次关系
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours, hierarchy)
        for i, contour in enumerate(contours):
            M = cv2.moments(contour)
            if M['m00'] == 0:
                cx = cy = 0
            else:
                cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            if 4000 < cv2.contourArea(contour) < 8000 and 220 < cv2.arcLength(contour, True) < 390:
                if cx < 200:
                    continue
                x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                return x
        return 0

    while deltax == 0:
        time.sleep(2)
        verify_image_url = elemenrt.get_attribute('src')
        verify_image = requests.get(verify_image_url).content
        path = f'{Root}/verify.jpg'
        MyCreatePath(path)
        with open(path, 'wb') as f:
            f.write(verify_image)
        verify_img = cv2.imread(path)
        deltax = get_pos(verify_img)
        if deltax == 0:
            print('x==0')
            page.refresh()

    result = int(deltax * 0.74)
    slide = page.find_element_by_id(id)
    ActionChains(page).move_to_element(slide).perform()
    time.sleep(0.2)
    pos = pyautogui.position()
    pyautogui.mouseDown(pos[0], pos[1])
    pyautogui.moveTo(pos[0] + result, pos[1])
    pyautogui.mouseUp()
    time.sleep(3)


def MyElement(l, depth=0, silent=None):
    """
    返回元素，找不到为None
    :param l:
    :return:
    """
    page = l[0]
    method = l[1]
    s = l[2]
    result = page.find_elements(method, s)
    if len(result):
        return result[0]
    else:
        depth += 1
        time.sleep(2)
        if silent == None:
            print(f'Element not found, retrying... method={method}, string={s}')
        if depth >= 10:
            return None
        else:
            return MyElement(l, depth, silent)


def MyElements(l, depth=0):
    """
    返回元素列表，找不到为[]
    :param l:
    :return:
    """
    page = l[0]
    method = l[1]
    s = l[2]
    result = page.find_elements(method, s)
    if len(result):
        return result
    else:
        depth += 1
        time.sleep(2)
        print(f'Element not found, retrying... method={method}, string={s}')
        if depth >= 10:
            return []
        else:
            return MyElements(l, depth)


def MySkip(l):
    """
    简单跳过，不做操作，等待人工操作来跳过，否则一直等待
    :param l:列表：页面，XPATH/ID，字符串
    :return:
    """
    page = l[0]
    method = l[1]
    s = l[2]
    time.sleep(1)
    if MyElement([page, method, s], depth=8, silent=True):
        print(s,'detected. 等待其消失中以继续。。。')
        WebDriverWait(page, 9999, 3).until_not(expected_conditions.presence_of_element_located(locator=(method, s)))


def MyGetScrollTop(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollTop;return(q)')


def MyGetScrollHeight(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollHeight;return(q)')


def MyScroll(l,silent=None):
    """

    :param l: 页面，第二个参数小于1可不传
    :return:
    """
    print('Scrolling..')
    ti=time.time()
    page = l[0]
    ratio = 1
    if len(l) > 1:
        ratio = l[1]
    ScrollTop = -1
    while ScrollTop != MyGetScrollTop([page]):
        ScrollTop = MyGetScrollTop([page])
        if not silent==None:
            print(ScrollTop)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != MyGetScrollTop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != MyGetScrollTop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != MyGetScrollTop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(1)
        if ScrollTop != MyGetScrollTop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        time.sleep(3)
        if ScrollTop != MyGetScrollTop([page]):
            continue
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
        time.sleep(1)
        page.execute_script(f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
    print(f'scrolling Done. Spent {time.time()-ti} s.')

def MyRequestDownload(LocalPath, mode, url):
    MyCreatePath(LocalPath)
    try:
        with open(LocalPath, mode) as f:
            f.write(requests.get(url=url, headers=headers).content)
    except(requests.exceptions.SSLError):
        try:
            with open(LocalPath, mode) as f:
                f.write(requests.get(url=url, headers=headers, verify=False).content)
        finally:
            input('SSLError')
            MyRequestDownload(LocalPath, mode, url)


def MyChrome(url='', time=100, mine=None, silent=None):
    try:
        options = webdriver.ChromeOptions()
        if not mine == None:
            options.add_argument(f"--user-data-dir=C:\\Users\\17371\\AppData\\Local\\Google\\Chrome\\User Data")
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
        if not silent == None:
            options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.set_page_load_timeout(time)
        driver.set_script_timeout(time)
        if not url == '':
            driver.get(url)
        return driver
    except selenium.common.exceptions.InvalidArgumentException:
        c = input('please close old page')
        return MyChrome()


def MyEdge(url='', silent=None):
    options = webdriver.EdgeOptions()
    if not silent == None:
        options.add_argument('headless')
    driver = webdriver.Edge(options=options)
    if not url == '':
        driver.get(url)
    return driver


def MyName(str):
    str = re.sub('/|\||\?|>|<|:|\n|/|"|\*', ' ', str)
    str = str.replace('  ', ' ')
    str = str.replace('\\', ' ')
    str = str.replace('\r', ' ')
    str = str.replace('\t', ' ')
    str = str.replace('\x08', ' ')
    str = str.replace('\x1c', ' ')

    return str[:224]


def MyClick(l):
    if len(l) > 2:
        try:
            MyElement(l).click()
            return
        except:
            try:
                ActionChains(l[0]).move_to_element(to_element=MyElement(l)).click().perform()
                return
            except:
                print('click error！')
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
            except:
                print('click error!')

    time.sleep(1)


def MyPress(l):
    page = l[0]
    s = l[1]
    if s == 'down':
        k = Keys.DOWN
    ActionChains(page).key_down(k).key_up(k).perform()


def MyTitle(l):
    page = l[0]
    element = MyElement([page, By.XPATH, '/html/head/title'])
    if element == None:
        return None
    return MyName(element.get_attribute('text'))


def MyPath(s=''):
    if s == '':
        s = __file__
    # s = s[:s.rfind('\\')]
    return s.replace('\\', '/')


def MySetScrollTop(l):
    page = l[0]
    x = l[1]
    page.execute_script(f'document.documentElement.scrollTop={x}')


def MyPageDownload(url, path, t=20, silent=True, depth=0):
    if depth > 2:
        return False
    path = MyPath(path)
    if path.find('.')<0:
        path+='/'
    root = os.path.abspath(path[:path.rfind('/')])
    name = path[path.rfind('/') + 1:]
    options = webdriver.ChromeOptions()
    # 设置下载路径
    prefs = {'download.default_directory': f'{root}'}
    options.add_experimental_option('prefs', prefs)
    if not silent == None:
        options.headless = True
    page = webdriver.Chrome(chrome_options=options)
    page.get(url)
    time.sleep(2)
    i = 0
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
            i += 1
    time.sleep(t)
    page.quit()
    time.sleep(1)
    # 如果下载失败，再下载一次30s
    if os.path.exists(path + '.crdownload'):
        os.remove(path + '.crdownload')
        print(f'[MyRequestDownload] download failed.No crdownload file left(auto deleted). you may try {url}')
        return MyPageDownload(url, path, t=30, depth=depth + 1)
    return True


def ThreadPageDownload(url, path):
    return _thread.start_new_thread(MyPageDownload, (url, path))


def MyBiFind(file, dest=[0x48, 0x12, 0x01, 0x06, 0x46, 0x46, 0x6D, 0x70]):
    myfile = open(file, 'rb')
    count = 0
    index = 0
    mystring = myfile.read(16)
    while (mystring):
        for x in mystring:
            count = count + 1
            if (x == dest[index]):
                index = index + 1
            else:
                index = 0
            if (index == len(dest)):
                return count - len(dest)
        mystring = myfile.read(16)

def MyTellSame(s1,s2):
    s1=str(s1)
    s2=str(s2)
    ratio=0.95
    if len(s1)>3 and len(s2)>3:
        if s1.rfind(s2)>0 or s2.rfind(s1)>0:
            return True
    # 进行保护，如果不是String直接返回False
    sum1=0
    # s1中能在s2里找到的个数
    sum2=0
    for i in s1:
        if i in s2:
            sum1+=1
    for i in s2:
        if i in s1:
            sum2+=1
    if sum1/len(s1)>ratio or sum2/len(s2)>ratio:
        return True
    else:
        return False

class MyTXT:
    def __init__(self, path):
        self.path = MyPath(path)
        self.loopcount = 0
        self.read()

    def read(self):
        # 读取l并处理
        self.l = MyFile('r', self.path)

        # 字符序列化
        newlist = []
        for i in self.l:
            i = str(i).strip('\n')
            if not i == '':
                newlist.append(str(i))
        self.l = newlist


    def save(self):
        l = []
        for i in self.l:
            l.append(str(i) + '\n')
        MyFile('w', self.path, l)

    def add(self, a):
        a=str(a).strip('\n')
        self.l.append(str(a))

    def delete(self):
        self.l=[]


class RefreshTXT:
    # 规定：
    # 实现：
    # .l全部字符串去尾换行符存储
    # 不进行排序
    # 希望实现实时生成副本可回滚

    def __init__(self, path):
        self.path = MyPath(path)
        self.loopcount = 0
        self.read()
        self.Rollback()
        self.set=set(self.l)

    def read(self):
        # 读取l并处理
        self.l = MyFile('rs', self.path)

        # 字符序列化
        newlist = []
        for i in self.l:
            i = str(i).strip('\n')
            if not i == '':
                newlist.append(str(i))
        self.l = newlist
        self.sortset()

    def delete(self, a):
        for i in self.l:
            if i == str(str(a).strip('\n')):
                self.l.remove(i)

    def sortset(self):
        newlist = list(set(self.l))
        newlist.sort(key=self.l.index)
        self.l = newlist

    def get(self):
        # 抽出最后一个，并加到首部
        if self.loopcount > self.length():
            return None
        a = self.l[-1]
        self.l.pop(-1)
        self.l.insert(0, a)
        self.loopcount += 1
        return a.strip('\n')

    def Rollback(self):
        if self.length()<2:
            return None
        self.loopcount += 1
        a = self.l[0]
        self.l.pop(0)
        self.l.append(a)
        return a.strip('\n')

    def length(self):
        return len(self.l)

    def save(self):
        self.sortset()
        l = []
        for i in self.l:
            l.append(str(i).strip('\n') + '\n')
        MyFile('w', self.path, l)

    def add(self, a):
        if type(a)==list:
            for e in a:
                if not e in self.set and not str(e) in self.set:
                    self.l.append(str(e).strip('\n'))
                    self.set.add(str(e).strip('\n'))
            return
        if not a in self.set and not str(a) in self.set:
            self.l.append(str(a).strip('\n'))
            self.set.add(str(a).strip('\n'))

    def insert(self, a):
        self.add(a)

    def exist(self, a):
        a = str(a)
        if a in self.l or a + '\n' in self.l:
            return True
        else:
            self.insert(a)
            return False

    def merge(self, path):
        l = RefreshTXT(path)
        self.l.extend(l.l)
        self.save()
        self.__init__(self.path)

    # def __del__(self):
    #     self.save()


# class MyDate():
#     def __init__(self):
#         localtime = time.localtime(time.time())
#         self.date=time.strftime("%Y-%m-%d", time.localtime())
#         self.time = time.strftime("%H-%M-%S", time.localtime())

def MyDate(s):
    localtime = time.localtime(time.time())
    return time.strftime("%Y-%m-%d"+str(s), time.localtime())

def MyTime(s=None):
    localtime = time.localtime(time.time())
    if s==None:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if s.find('hms')>=0:
        return time.strftime("%H:%M:%S", time.localtime())
    if s.find('ms')>=0:
        return time.strftime("%M:%S", time.localtime())
    if s.find('hm')>=0:
        return time.strftime("%H:%M", time.localtime())
    if s.find('h')>=0:
        return time.strftime("%H", time.localtime())
    if s.find('m')>=0:
        return time.strftime("%M", time.localtime())
    if s.find('s')>=0:
        return time.strftime("%S", time.localtime())




class MyPool():

    def __init__(self, max_workers,show=None):
        self.cool=0
        self.max_workers = max_workers
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self.show=show


    def excute(self, fn, /, *args, **kwargs):
        while self.isFulling():
            if not self.show == None:
                print('[MyPool] 警报。excute被挂起，因为线程池已满')
            time.sleep(5)
        self.cool+=1
        def do(fn,/,*args,**kwargs):
            if not self.show == None:
                print(f'[MyPool] 当前线程开始。剩余线程 {self.cool}')
            fn(*args,**kwargs)
            self.cool-=1
            if not self.show == None:
                print(f'[MyPool]当前线程结束。剩余线程 {self.cool}')

        self.pool.submit(do,fn, *args,**kwargs)

    def isFulling(self):
        return self.cool>=self.max_workers

    def wait(self,show=None):
        while self.cool:
            if show:
                print(f'[MyPool] 等待线程池腾空{self.cool}')
            time.sleep(3)
            while self.cool:
                if show:
                    print(f'[MyPool] 等待线程池腾空{self.cool}')
                time.sleep(3)



def MyKeyInput(x,y,s):
    pyperclip.copy(s)
    pyautogui.click(x,y)
    time.sleep(1)
    pyautogui.hotkey('ctrl'+'v')
    time.sleep(0.5)
    pyautogui.hotkey('Enter')
    time.sleep(1)

def MyPathExist(path,s,ratio=0.85):

    for (root,dirs,files)in os.walk(path):
        for dir in dirs:
            if Levenshtein.ratio(s,dir)>ratio:
                return True
        for file in files:
            if Levenshtein.ratio(s,file)>ratio:
                return True
    return False

def DesktopPath(s=''):
    return 'C:/Users/17371/Desktop/'+s

def PicCachePath(s=''):
    return './PicCache/'+s

def MyScreenShot(path,l=[],show=None,cut=0,whole=None,element=None):
    def Show():
        nonlocal path
        if not show==None:
            Image.open(path).show()

    # 第一种元素截图
    if not element==None:
        MyFile('wb',path,element.screenshot_as_png)
        Show()
        return

    page=l[0]

    # 网页截图
    if not whole==None:
        page.get_screenshot_as_file(path)
        Show()
        return



    # # 元素截图
    method=l[1]
    s=l[2]
    MyFile('wb',path,MyElement([page,method,s]).screenshot_as_png)
    Show()
    # height=element.rect['height']
    # y=element.location['y']
    # sum=0
    # while sum<height:
    #     MySetScrollTop(max(0,y+sum-cut))

def MyDeleteEmpty(s):
    lis=[]
    for (root,dirs,files)in os.walk(os.path.abspath(s)):
        if files==[]and dirs==[]:
            lis.append(root)
    for i in lis:
        os.rmdir(i)

def MyVideoCut(inputpath,outputpath,start,end):

    sourcepath=os.path.abspath(inputpath)
    command=f'ffmpeg  -i {inputpath} -vcodec copy -acodec copy -ss {start} -to {end} {outputpath} -y'
    os.system('"%s"' % command)


def Myre(s,pattern):
    return (re.compile(pattern).findall(s))

def DiscInfo(s):
    gb = 1024 ** 3  # GB == gigabyte
    try:
        total_b, used_b, free_b = shutil.disk_usage(s.strip('\n')+':')  # 查看磁盘的使用情况
    except:
        return 0
    # print('总的磁盘空间: {:6.2f} GB '.format(total_b / gb))
    # print('已经使用的 : {:6.2f} GB '.format(used_b / gb))
    # print('未使用的 : {:6.2f} GB '.format(free_b / gb))
    return (free_b / gb)


global ti
ti = {}
def settime(n=time.time()):
    global ti
    n=hash(n)
    ti.update({n:time.time()})
    return n

def calltime(n):
    global ti
    return time.time() - ti.get(n)

# os.chdir(input('请输入操作盘，只输入一个大写字母。') + ':/')

for i in RefreshTXT('D:/Kaleidoscope/ActivDisc.txt').l:
    if DiscInfo(i)>=1:
        os.chdir(i+':/')
        break

def dosth():
    time.sleep(2)

def log(s):
    print(f'{MyTime("hms")}  {inspect.getframeinfo(inspect.currentframe().f_back)[2]}\n\t{s}')

log('MyUtils already loaded')


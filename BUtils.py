import MyUtils
from selenium.webdriver.common.by import By

def AddUser(url, file):
    # 从给定的网址输入
    print('[BUtils AddUser]请确认已经在Chrome登录。')
    page=MyUtils.MyChrome(url,mine=1,silent=None)
    ll=MyUtils.MyElements([page,By.XPATH,'/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div[2]/ul[1]/li'])
    for el in ll:
        ell=MyUtils.MyElement([el,By.TAG_NAME,'a'])
        con=ell.get_attribute('href').strip('/')
        upid=con[con.rfind('/')+1:]
        file.add(upid)
    file.save()
    page.close()
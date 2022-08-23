import os.path
import time
from selenium.webdriver.common.by import By

import MyUtils
for i in range(2,60):

    url=f'https://3g.ali213.net/gl/html/673909_{i}.html'
    page=MyUtils.edge(url)
    page.set_window_size(400,700)
    time.sleep(1)
    MyUtils.click([page, By.CLASS_NAME, 'read-all'])
    time.sleep(1)


    # wenming=MyUtils.MyElement([page,By.XPATH,'/html/body/div[7]/div[9]/p[2]/span/strong']).text
    # wenming=wenming.strip('文明介绍')
    wenming=MyUtils.MyTitle([page])
    wenming=wenming[wenming.find('-')+1:wenming.find(' ')]
    txt=[]
    for i in MyUtils.Elements([page, By.TAG_NAME, 'p']):
        txt.append(i.text)


    if os.path.exists(MyUtils.DesktopPath('huamndkind/'+wenming+'.txt')):
        continue
    content=MyUtils.txt(MyUtils.DesktopPath('huamndkind/' + wenming + '.txt'))
    t=MyUtils.txt(MyUtils.DesktopPath('huamndkind/' + '总计' + '.txt'))
    c=False
    next=False
    b=False
    xiayixiang=False
    for i in txt:
        if i=='':
            continue
        # 初始化
        if i==wenming+'文明介绍':
            c=True
        if i[:4]=='本质特性':
            benzhi=i[-5:-3]
            c=False
            continue
        if i[:4]=='传承特性':
            chuancheng=i[5:]
            xiayixiang=True
            continue
        if xiayixiang:
            xiayixiang=False
            chuancheng+=' ： '+i
            continue
        if i[:5]=='象征性单位':
            danwei=i[6:]
            c=True
            continue
        if i[:2]in['属性','花费','解锁']:
            if c:
                shuxing=i[3:]
            c=False
            continue
        if i[:4]=='详细信息':
            xiangxi=i[5:]
            continue
        if i[:5]=='象征性区域':
            quyu=i[6:]
            c=True
            continue
        if i[:2]=='效果':
            xiaoguo=i[3:]
            c=False
            continue

        if c:
            if i=='你知道吗？':
                content.add('\n')
                c=False
            content.add(i)

    t.add(f'{wenming}  {benzhi}主义者 \n {chuancheng} \n {quyu} ： {xiaoguo}\n {danwei} ： {shuxing}  {xiangxi}')
    t.save()
    content.save()
    page.close()
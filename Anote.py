import pyperclip

import MyUtils
# 初始化
path=MyUtils.standarlizedPath('D:\Kaleidoscope\self/语录&随笔随想')
root=('D:\Kaleidoscope\self/语录&随笔随想')
f0=MyUtils.txt(root + '/count.txt')
inc=0
c=''
cc=''
while True:

    # 先获取总数
    count=int((f0.l)[0])

    # 找到对应文件
    hun=count//100
    sname=f'/{hun*100+1}-{hun*100+100}.txt'
    f1=MyUtils.txt(root + sname)

    # 进行增加
    # print(MyUtils.MyTime())
    c=''
    cc=''
    while not (cc=='FE' or cc=='EF' or cc=='ef' or cc=='fe'):
        cc=input('请输入文案，以末尾的FE作为结束：')
        ccc=cc.strip('FE')
        ccc=cc.strip('EF')
        ccc=cc.strip('ef')
        ccc=cc.strip('fe')
        c+='\n'+cc
        if not ccc==cc:
            break
    c=c.strip('FE')
    c=c.strip('EF')
    c=c.strip('ef')
    c=c.strip('fe')
    c=c.replace('\n','\n\t')
    c=c+'\n'
    if c==c.strip('TEST'):
        f1.add(MyUtils.MyTime()+str(c))
        f1.save()
        count+=1
        f0.delete()
        f0.add(count)
        f0.save()
    # path=MyUtils.MyPath("D:\\Kaleidoscope\\self\\语录&随笔随想")+sname
    print(f'[Main] [第{count}条]{MyUtils.MyTime()} 已保存。现在你可以在{f1.path}查看。')
    pyperclip.copy(f1.path)
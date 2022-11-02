import pyperclip

import MyUtils

# 初始化
path = MyUtils.standarlizedPath('D:/Kaleidoscope/self/记录 语录 随笔 随想')
root = (r'D:/Kaleidoscope/self/记录 语录 随笔 随想')
f0 = MyUtils.txt(root + '/count.txt')
inc = 0
c = ''
cc = ''
while True:

    # 先获取总数
    count = int((f0.l)[0])

    # 找到对应文件
    hun = count // 100
    sname = f'/{hun * 100 + 1}-{hun * 100 + 100}.txt'
    f1 = MyUtils.txt(root + sname)
    pyperclip.copy(f1.path)

    # 进行增加
    # print(MyUtils.MyTime())
    c = ''
    cc = ''
    while not cc[-2:] in ['FE', 'FE', 'ef', 'fe']:
        cc = input('请输入文案，以末尾的FE作为结束：')
        ccc = cc.strip('FE').strip('EF').strip('fe').strip('ef')
        c += '\n' + cc
        if not ccc == cc:
            break
    c = c.strip('FE').strip('EF').strip('fe').strip('ef')
    c = c.replace('\n', '\n\t')
    c = c + '\n'
    if c == c.strip('TEST'):
        f1.add(MyUtils.nowstr() + str(c))
        count += 1
        f0.clear()
        f0.add(count)
        f0.save()
    # path=MyUtils.MyPath("D:\\Kaleidoscope\\self\\语录&随笔随想")+sname
    MyUtils.log(f'[第{count}条]{MyUtils.nowstr()} 已保存。现在你可以在{f1.path}查看。')
    pyperclip.copy(f1.path)

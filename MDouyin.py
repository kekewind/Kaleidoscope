import os

import pyperclip

import DouyinUtils
import MyUtils

allpieces = DouyinUtils.allpieces
allusers = DouyinUtils.allusers
missing = DouyinUtils.missing


# 删除不存在操作盘的作品记录
def deleteRecorded():
    deletelis = []
    count = 0
    for d in allpieces.d:
        count += 1
        if count % 1000 == 0:
            print(f'{count}/{allpieces.length()}')
        for i in allpieces.d[d]:
            if type(i) == list:
                print(i)
            if not i['disk'] == MyUtils.diskname:
                continue
            author, title = i['author'], i['title']
            if [] == MyUtils.listfile(f'./抖音/{author}/{d}_{title}') and not os.path.exists(f'./抖音/{author}/{d}_{title}.mp4'):
                j = ({d: {"disk": MyUtils.diskname, 'author': author, "title": title}})
                deletelis.append(j)
                missing.add(j)
    for i in deletelis:
        allpieces.delete(i)


#  删除下载的missing
def deleteMissing():
    lis1 = []
    for i in missing.l:
        d = MyUtils.jsontodict(i)
        d = MyUtils.value(d)[0]
        path = MyUtils.standarlizedPath(f'./抖音/{d["author"]}/{d["title"]}')
        if os.path.exists(path):
            lis1.append(i)
        if os.path.exists(path + '.mp4'):
            lis1.append(i)
    print(f'后来新增的{lis1}')
    print(len(lis1))
    for j in lis1:
        MyUtils.rtxt.delete(missing, j)


# 手动添加作者
def adduser():
    while True:
        c = input()
        DouyinUtils.allusers.add({c: []})


# 统计总数
def count():
    MyUtils.log(f'作品总数：{allpieces.length()}')
    MyUtils.log(f"作者总数：{allusers.length()}")
    MyUtils.log(f"失败总数：{missing.length()}")
    # pyperclip.copy(f'{allpieces.length()}\n{allusers.length()}\n{missing.length()}')
    file=0
    dir=0
    for i in MyUtils.listdir('./抖音'):
        dir+=len(MyUtils.listdir(i))
        file+=len(MyUtils.listfile(i))
    MyUtils.log(f"视频总数：{file}")
    MyUtils.log(f"图片总数：{dir}")


# 统计重复的作品
def findduplicate():
    lis = []
    lis1 = []
    # 先统计操作盘
    for user in MyUtils.listdir('./抖音/'):
        for title in MyUtils.listdir(user):
            lis.append((MyUtils.filename(user), MyUtils.filename(title)))
        for title in MyUtils.listfile(user):
            lis.append((MyUtils.filename(user), MyUtils.filename(title).strip('.mp4')))
    MyUtils.delog('操作盘统计完毕')
    #    再统计记录
    for i in DouyinUtils.allpieces.l:
        d = MyUtils.jsontodict(i)
        d = d[MyUtils.keys(d)[0]]
        if d['disk'] == MyUtils.diskname:
            continue
        p = (d['author'], d['title'])
        if p in lis:
            lis1.append(MyUtils.dicttojson({'author': p[0], 'title': p[1], 'disk': d['disk']}) + '\n')
    MyUtils.delog('记录统计完毕')
    # 输出结果
    MyUtils.txt(MyUtils.desktoppath('new')).add(lis1)
    print(lis1)


def main():
    # deleteRecorded()
    # deleteMissing()
    count()
    # findduplicate()


#     辅助函数（不必要的过程函数）

if __name__ == '__main__':
    main()

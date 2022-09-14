import os

import DouyinUtils
import MyUtils
allpieces=DouyinUtils.allpieces
allusers=DouyinUtils.allusers
missing=DouyinUtils.missing

# 删除不存在操作盘的作品记录
def delete():
    deletelis=[]
    for d in allpieces.d:
        if not allpieces.d[d]['disk']==MyUtils.diskname:
            continue
        author,title=allpieces.d[d]['author'],allpieces.d[d]['title']
        if not os.path.exists(f'./抖音/{author}/{title}')and not os.path.exists(f'./抖音/{author}/{title}.mp4'):
            j=({d:{"disk":MyUtils.diskname,'author':author,"title":title}})
            deletelis.append(j)
            missing.add(j)
    for i in deletelis:
        allpieces.delete(i)

# 手动添加作者
def adduser():
    while True:
        c=input()
        DouyinUtils.allusers.add({c:[]})

# 统计总数
def count():
    MyUtils.log(f'作品总数：{allpieces.length()}')
    MyUtils.log(f"作者总数：{allusers.length()}")
    MyUtils.log(f'')

# 统计重复的作品
def findduplicate():
    lis=[]
    lis1=[]
    # 先统计操作盘
    for user in MyUtils.listdir('./抖音/'):
        for title in MyUtils.listdir(user):
            lis.append((MyUtils.filename(user),MyUtils.filename(title)))
        for title in MyUtils.listfile(user):
            lis.append((MyUtils.filename(user),MyUtils.filename(title).strip('.mp4')))
    MyUtils.delog('操作盘统计完毕')
    #    再统计记录
    for i in DouyinUtils.allpieces.l:
        d=MyUtils.jsontodict(i)
        d=d[MyUtils.keys(d)[0]]
        if d['disk']==MyUtils.diskname:
            continue
        p=((d['author'],d['title']))
        if p in lis:
            lis1.append(MyUtils.dicttojson({'author':p[0],'title':p[1],'disk':d['disk']})+'\n')
    MyUtils.delog('记录统计完毕')
    # 输出结果
    MyUtils.txt(MyUtils.desktoppath('new')).add(lis1)
    print(lis1)



def main():
    # delete()
    count()
    # findduplicate()

if __name__=='__main__':
    main()
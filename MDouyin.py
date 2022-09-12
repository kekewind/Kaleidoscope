import os

import DouyinUtils
import MyUtils
allpieces=DouyinUtils.allpieces
allusers=DouyinUtils.allusers
missing=DouyinUtils.missing

# 删除不存在的作品记录
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

def main():
    count()

if __name__=='__main__':
    main()
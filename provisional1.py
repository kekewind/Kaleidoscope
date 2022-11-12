
import MyUtils
for i in MyUtils.listdir(MyUtils.desktoppath('地理空间数据库/zhaoxiang/待生成新作业')):
    for j in MyUtils.listfile(i):
        MyUtils.copyfile(j,MyUtils.desktoppath(f'地理空间数据库/zhaoxiang/生成新作业/{MyUtils.filename(i)}/{MyUtils.filename(j)}'))
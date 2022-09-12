import MyUtils

# 在操作盘璐琪文件夹下
for file in MyUtils.listfile(['./','./璐琪/']):
    if 'Scree' in file or 'SVID' in file:
        a = MyUtils.filename(file)
        if 'SVID' in a:
            year, month, day = a[5:9], a[9:11], a[11:13]
        if 'Scre' in a:
            year, month, day = a[15:19], a[20:22], a[23:25]

        MyUtils.move(file, f'./璐琪/{year}-{month}-{day}')


f=MyUtils.rjson(MyUtils.root+'璐琪/record')
for dir in MyUtils.listdir(['./璐琪/']):
    for file in MyUtils.listfile(dir):
        # f.add({file:MyUtils.diskname})
        print({file:MyUtils.diskname})
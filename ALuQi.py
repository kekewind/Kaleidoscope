import MyUtils

# 规整移动操作盘中的文件
for file in MyUtils.listfile(['./', './璐琪/']):
    if 'Scree' in file or 'SVID' in file:
        filename = MyUtils.filename(file)
        if 'SVID' in filename:
            year, month, day = filename[5:9], filename[9:11], filename[11:13]
        if 'Scre' in filename:
            year, month, day = filename[15:19], filename[20:22], filename[23:25]
        # MyUtils.log(f"move({file}, './璐琪/{year}-{month}-{day}')")
        targetdir=f'./璐琪/{year}-{month}-{day}'
        if not MyUtils.isfile(targetdir + filename):
            MyUtils.move(file, targetdir)

# 对规整路径的操作盘文件进行记录添加
f = MyUtils.rjson(MyUtils.root + '璐琪/record')
for dir in MyUtils.listdir(['./璐琪/']):
    for file in MyUtils.listfile(dir):
        f.add({MyUtils.filename(file): MyUtils.diskname})

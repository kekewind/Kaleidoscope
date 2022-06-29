import os.path
import time

import MyUtils

# 链接RefreshTXT
droot = 'F:\\虎牙\\downloading'
file = MyUtils.RefreshTXT(droot+'\\m3u8.txt')

# 逐个找到空文件夹
i = 0
l = []
while i < 1002:
    i += 1
    if os.path.exists(droot + f'\\{i + 1}'):
        for (roots, dirs, files) in os.walk(droot + f'\\{i + 1}'):
            if files == []:
                l.append(roots)

# 逐个PageDownload
e = MyUtils.MyPool(50)
while file.loopcount < file.length():
    # 如果已下载，跳过
    if os.path.exists(droot + f'\\{file.loopcount + 1}') and not (droot + f'\\{file.loopcount + 1}') in l:
        file.Rollback()
        continue
    e.excute(MyUtils.MyPageDownload, file.Rollback(), droot + f'\\{file.loopcount}\\{file.loopcount}.ts')
    print(droot + f'\\{file.loopcount}\\{file.loopcount}.ts下载中')
    # 限制片段
    if file.loopcount%10==0:
        # print('cooling down')
        time.sleep(2)
    if file.loopcount > 1000:
        break
while not os.path.exists(droot+'\\1001'):
    time.sleep(10)
time.sleep(5)
# 批处理

# 小合并


# 大合并
# 获取最大编号文件夹
for (roots, dirs, files) in os.walk(droot):
    # 弹出新建文件夹
    dirs.pop(-1)
    l = []
    for i in dirs:
        l.append(int(i))
    break

# 生成字符串
slist = []
s = ''
count = 0
for i in range(max(l)):
    count += 1
    for (roots, dirs, files) in os.walk(droot + f'\\{i}'):
        s += MyUtils.MyPath(droot + '\\' + str(i) + '\\' + files[0]) + '|'
    if count > 100:
        count = 0
        slist.append(s)
        s = ''

# 批处理
# i=0
# for s in slist:
#     i+=1
#     ss=(f'ffmpeg -i "concat:{s}" -acodec copy -vcodec copy -absf aac_adtstoasc F:/虎牙/clip/{i}.mp4')
#     os.system(f'ffmpeg -i "concat:{s}" -acodec copy -vcodec copy -absf aac_adtstoasc F:/虎牙/clip/{i}.ts')

# mp4->ts
path = 'F:/虎牙'
s = ''
for droot, dirs, files in os.walk(f'{path}/clip'):
    for file in files:
        if not os.path.exists(f'{path}/clip/{file.replace("mp4", "ts")}'):
            os.system(f'ffmpeg -i {path}/clip/{file} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {path}/clip/{file.replace("mp4", "ts")}')
            s += path + '/clip/' + file.replace("mp4", "ts") + '|'

# 合成大文件
l = ''
for (roots, dirs, files) in os.walk('F:/虎牙/clip'):
    for file in files:
        if file[-3:] == '.ts':
            l += MyUtils.MyPath(roots + '\\' + file + '|')
os.system(f'ffmpeg -i "concat:{l}" -acodec copy -vcodec copy -absf aac_adtstoasc F:/虎牙/output.mp4')

import os

import MyUtils

while True:
    inputload='../璐琪/'
    outputname=MyUtils.DesktopPath('collection/'+MyUtils.MyName(MyUtils.MyTime())+'.mp4')
    outputname=outputname.replace(' ','')

    name=input('\n输入文件名：').strip('.mp4')
    start=input('输入开始时间：')
    end=input('输入结束时间：')

    flag=True
    for (root,dirs,files) in os.walk(inputload):
        for file in files:
            print(file)
            if file==name+'.mp4':
                flag=False
                break
        if not flag:
            break

    sourcepath=os.path.abspath(root+'/'+file)
    command=f'ffmpeg  -i {sourcepath} -vcodec copy -acodec copy -ss {start} -to {end} {outputname} -y'
    os.system('"%s"' % command)


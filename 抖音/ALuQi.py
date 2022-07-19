import datetime
import os
import shutil

import MyUtils
for (root,dirs,files)in os.walk('璐琪/'):
    for file in files:
        if file.find('mp4')>1:
            if MyUtils.TellStringSame('Screenrecorder',file):
                year=int(file[15:19])
                month=int(file[20:22])
                day=int(file[23:25])
                hour=int(file[26:28])
            if MyUtils.TellStringSame('SVID',file):
                year=int(file[5:9])
                month=int(file[9:11])
                day=int(file[11:13])
                hour=int(file[14:16])
            if int(hour)<12:
                t=datetime.datetime(year,int(month),int(day))
                t=t+datetime.timedelta(days=-1)
                year=t.year
                month=t.month
                day=t.day
            dirname=f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'
            if not os.path.exists(f'璐琪/{dirname}'):
                os.mkdir(f'璐琪/{dirname}')
            shutil.move(f'璐琪/{file}',f'璐琪/{dirname}')
            MyUtils.log(f'{file} already processed. to {dirname}')
    break
for (root,dirs,files)in os.walk('璐琪/Screenshots'):
    for file in files:
        if file.find('mp4')>1:
            if MyUtils.TellStringSame('Screenrecorder',file):
                year=int(file[15:19])
                month=int(file[20:22])
                day=int(file[23:25])
                hour=int(file[26:28])
            if MyUtils.TellStringSame('SVID',file):
                year=int(file[5:9])
                month=int(file[9:11])
                day=int(file[11:13])
                hour=int(file[14:16])
            if int(hour)<12:
                t=datetime.datetime(year,int(month),int(day))
                t=t+datetime.timedelta(days=-1)
                year=t.year
                month=t.month
                day=t.day
            dirname=f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'
            if not os.path.exists(f'璐琪/{dirname}'):
                os.mkdir(f'璐琪/{dirname}')
            shutil.move(f'璐琪/Screenshots/{file}',f'璐琪/{dirname}')
            MyUtils.log(f'{file} already processed. to {dirname}')
    break
if os.path.exists(f'璐琪/Screenshots'):
    os.remove(f'璐琪/Screenshots')
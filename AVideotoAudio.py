import moviepy.editor
import os
import MyUtils

path = "F:\-柚子-呐"
# 统计已转换个数
i = 0
for (root, dirs, files) in os.walk(path):
    for file in files:
        i += 1
# 遍历，.mp4全改成日期\\编号.mp3
for (root, dirs, files) in os.walk(fr'C:\Users\{MyUtils.user}\Videos\Captures\A'):
    for file in files:
        if not file.find('mp4'):
            continue
        i += 1
        my_clip = moviepy.editor.VideoFileClip(fr'C:\Users\{MyUtils.user}\Videos\Captures\A' + '\\' + file)
        # 这好像是一个对象
        # file[:-4]是文件名
        my_clip.audio.write_audiofile(path + '\\' + MyUtils.MyDate() + '\\' + str(i) + '.mp3')
        print(f"Done:{file}")
# 删除mp4
# for (droot, dirs, files) in os.walk(r'C:\Users\17371\Videos\Captures\A'):
#     for file in files:
#         if file.find('mp4'):
#             os.remove(r'C:\Users\17371\Videos\Captures\A' + '\\' + file)

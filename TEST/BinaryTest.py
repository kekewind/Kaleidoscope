import sys

import MyUtils
import os

import moviepy.editor
import moviepy.video.compositing.concatenate
import moviepy.video.io.VideoFileClip

l = MyUtils.file('rb', 'D:\standardizedPF\Spectrum/2.mp4')


def find(dest=[0x48, 0x12, 0x01, 0x06, 0x46, 0x46, 0x6D, 0x70]):
    myfile = open('D:\standardizedPF\Spectrum/2.mp4', 'rb')
    count = 0
    index = 0
    mystring = myfile.read(16)
    while (mystring):
        for x in mystring:
            count = count + 1
            if (x == dest[index]):
                index = index + 1
            else:
                index = 0
            if (index == len(dest)):
                return count - len(dest)
        mystring = myfile.read(16)


print(find())

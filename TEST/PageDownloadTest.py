import MyUtils

s = 'https://v26-web.douyinvod.com/9723003d122c2c7c9d54b29c06a04b2a/62efb7e8/video/tos/cn/tos-cn-ve-15c001-alinc2/03845f0d19414f81a186ce8324ba2956/?a=6383&ch=26&cr=0&dr=0&lr=all&cd=0%7C0%7C0%7C0&br=2092&bt=2092&cs=0&ds=3&ft=iDIGbiNN6VQ9wUsKz3lW.CIbi7thbhdxwiMF_4kag36&mime_type=video_mp4&qs=0&rc=ZTc3ZGQ7PGdoZzo8PGRoaEBpajs3djk6ZjVzPDMzNGkzM0AwX2IvYTZiXl4xYWBfMDZfYSNeX2NfcjQwMDRgLS1kLTBzcw%3D%3D&l=021659873560104fdbddc0200ff2f010a97f1250000008932f8af'
MyUtils.pagedownload(s, MyUtils.DesktopPath('1.mp4'))

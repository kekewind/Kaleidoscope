import time
import MyUtils
import PySimpleGUI
import multiprocessing

def console(s,duration=999,text_color='#F08080',font=('Hack',14),size=28):
    #  每当新的控制台启动后，改内容，然后开新进程，将0改为1，1改为0
    # 控制台每隔一段时间刷新，如果变为0则退出。
    # 新的控制台计时结束后，将1改为0
    refreshtime=0.6
    MyUtils.consoletxt.add({MyUtils.nowstr():s})
    while 3600<MyUtils.Now().counttime(MyUtils.Time(MyUtils.key(MyUtils.jsontodict(MyUtils.consoletxt.get())))):
        MyUtils.consoletxt.l.pop(0)
    MyUtils.consoletxt.save()
    #短暂显示桌面控制台
    def show():
        # 系统默认颜色
        # COLOR_SYSTEM_DEFAULT='1234567890'=='ADD123'
        global win
        outs=''
        inc=0
        for i in MyUtils.consoletxt.l:
            outs+=f'[{inc}]  {MyUtils.value(i)}\n'
            inc+=1
        layout = [[PySimpleGUI.Text(outs, background_color='#add123', pad=(0, 0),
                                    text_color=text_color,font=font)]]
        win = PySimpleGUI.Window('', layout, no_titlebar=True, keep_on_top=True,
            location=(120*16/3*2, 0), auto_close=True, auto_close_duration=duration,
            transparent_color='#add123', margins=(0, 0))
        event, values = win.read(timeout=0)
        time.sleep(0.3)
        return win
    def func(duration,):
        print('1')
        return
        # 更改consolerunning
        if consolerunning.l[0] == '1':
            consolerunning.l[0] == '0'
            consolerunning.save()
        elif consolerunning.l[0] == '0':
            consolerunning.l[0] == '1'
            consolerunning.save()
        while duration > 0:
            time.sleep(refreshtime)
            duration -= refreshtime
            show()
    process=multiprocessing.Process(target=func,args=(duration,))
    # process.daemon=True
    process.start()
win = console('Here is the message.')
time.sleep(30)

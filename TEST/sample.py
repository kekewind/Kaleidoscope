import time

import PySimpleGUI as sg

def console(message):
    global win
    layout = [[sg.Text(message, background_color=bg, pad=(0, 0),\
                       text_color='grey85',font='vijaya')]]
    win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True,
        location=(120*8, 0), auto_close=False, auto_close_duration=999,
        transparent_color='#add123', margins=(0, 0))
    event, values = win.read(timeout=0)
    return win

bg = '#add123'
win = console('Here is the message.')

time.sleep(10)

import MyUtils

a = MyUtils.RefreshJson(MyUtils.desktoppath('a'))
# b=MyUtils.RefreshJson(MyUtils.desktoppath('b'))
for i in range(10):
    a.add({str(i): i})

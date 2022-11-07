import MyUtils

jso = MyUtils.Json(MyUtils.DesktopPath('ab.txt'))
# jso=MyUtils.RefreshJson(MyUtils.DesktopPath('ab.txt'))
print(jso.get())

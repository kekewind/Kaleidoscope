import MyUtils
import DouyinUtils

jso = MyUtils.RefreshJson(MyUtils.DesktopPath('ab.txt'))
# jso=MyUtils.RefreshJson(MyUtils.DesktopPath('ab.txt'))
jso.add({"1": [1]})
jso.add({"1": []})

print(jso.l)
print(jso.d)

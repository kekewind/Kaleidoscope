import MyUtils

t = MyUtils.RefreshTXT(MyUtils.DesktopPath('ab.txt'))
# count=MyUtils.txt(MyUtils.DesktopPath('ab.txt'))

print(t.l)
for i in range(10):
    t.add(MyUtils.dicttojson({"0": i}))

for i in t.l:
    print(t.get())
print(t.l)

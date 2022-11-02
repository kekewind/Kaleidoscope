import MyUtils

d1 = {'1': 2}
d2 = {'1': 3}
d3 = {list(d1.keys())[0]: 4}
d4 = {MyUtils.key(d1): 5}
d5 = {MyUtils.key(d1): 6}
# print(d2.keys())
l1 = [d3, d4]
print(MyUtils.set(l1))

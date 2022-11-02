# 模拟
import queue


def read():
    s = input()
    lis = s.split(' ')
    ret = []
    for i in lis:
        ret.append(int(i))
    return ret


(m, n, k) = read()
# 堆栈容量
#  队列长度
#  读入行数

# 对于每行
for kk in range(k):
    lis = read()
    q = []
    index = 0
    i = 1
    t = True
    while index < n:
        if q == []:
            q.append(i)
            i += 1
            continue
        # 如果小于 return False break
        if q[-1] > lis[index] or len(q) > m:
            print('NO')
            t = False
            break
        # 如果下一个大于当前栈顶，则不断add
        if q[-1] < lis[index]:
            q.append(i)
            i += 1
            continue
        # 如果等于，pop，continue
        if q[-1] == lis[index]:
            q.pop(-1)
            index += 1
            continue
    if t:
        print('YES')

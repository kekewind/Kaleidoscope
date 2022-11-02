import requests
import MyUtils
import csv
import os


def get_data(dpAddress, sql):
    """
    get data from dp address
    @param dpAddress  DP Address访问地址
    """
    # url = "https://www.citybrain.org/api/getData"
    url = "http://192.168.15.41:43000/api/getData"

    data = {"dpAddress": dpAddress, "payload": "{\"selectSql\":\"" + sql + "\"}"}
    resp = requests.post(url=url, headers={"content-type": "application/json"}, json=data)
    print(resp)
    result = resp.json()
    return result["data"]


# f=MyUtils.txt(MyUtils.desktoppath('ab.txt'))

i = 1999
for j in range(1, 2):
    path = MyUtils.desktoppath(f'./shuiwen/{i}/{j}.csv')
    os.remove(path)
    out = open(path, 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    cmd = f"select * from shuiwen_data where year={i} and month={j} and x>(73+180)*120 and x<(153+180)*120 and y>(3+90)*120 and y<(53+90)*120;"
    print(cmd)
    data = get_data("1566D2A547021000", cmd)
    MyUtils.log(f'request{i}-{j} done.')
    f = MyUtils.txt(MyUtils.desktoppath(f'/shuiwen/{i}/{j}.txt'))
    data = eval(data)
    for lis in data:
        k = lis.split(';')
        try:
            (x, y) = (int(k[2]), int(k[3]))
            x = x / 120.0 - 180
            y = y / 120.0 - 90
            (k[2], k[3]) = (str(x)[:], str(y)[:],)
        except:
            pass
        csv_write.writerow(k)

        f.add(k)

    out.close()

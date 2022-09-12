scale=5
import MyUtils
import requests
import csv
odpscmd=MyUtils.txt(MyUtils.desktoppath('odpscmd.txt'))
cmd=MyUtils.txt(MyUtils.desktoppath('cmd.txt'))
yearmonth=[]
for i in odpscmd.l:
    print(i)
    yearmonth.append(eval(i))
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
# lon x
# lat y
# 18360  39960
# 11160  17160
# 73-153
# 3-53
# 生成边框数组
l1=[]
for i in range(73,153+scale,scale):
    l1.append(i)
print(l1)
l2=[]
for i in range(3,53+scale,scale):
    l2.append(i)
print(l2)

def lontox(lon):
    return int(lon+180)*120
def lattoy(lat):
    return int(lat+90)*120
def xtolon(x):
    return int(x/120-180)
def ytolat(y):
    return int(y/120-90)



        # selecter=f'create table chelsa_china_{year}_{month}  lifecycle 20 as select month,lon,lat,pr,tas,tasmax,tasmin from chelsa_china where year={year} and month={month};'
        # odpscmd.add(selecter)


for year,month in yearmonth:
    selecter=f'''
    tunnel download chelsa_china_{year}_{month}_a /root/{year}_{month}.csv;'''
#     selecter=f"""create table chelsa_china_{year}_{month}_a lifecycle 20
# as select int(leftb/120-180),int(upb/120-90),sum(pr)
# from chelsa_china_{year}_{month}_accumulated group by leftb,rightb,upb,downb;"""
    cmd.add(selecter)

#     for i in l1:
#         for j in l2:
#             left,right,up,down=i,i+scale,j+scale,j
#             leftb,rightb,upb,downb=lontox(left),lontox(right),lattoy(up),lattoy(down)
#             center=(i+scale/2.0,j+scale/2.0)
#             selecter = f'create table chelsa_china_{year}_{month}_accumulated  lifecycle 20 as select ,pr,tas,tasmax,tasmin from chelsa_china where year={year} and month={month}\
#             and lon>{leftb} and lon<{rightb} and lat>{downb} and lat<{upb};'

# path = MyUtils.desktoppath('cordi.csv')
# out = open(path, 'a', newline='')
# csv_write = csv.writer(out, dialect='excel')
# for i in l1:
#     for j in l2:
#         left,right,up,down=i,i+scale,j+scale,j
#         leftb,rightb,upb,downb=lontox(left),lontox(right),lattoy(up),lattoy(down)
#         csv_write.writerow([leftb,rightb,upb,downb])
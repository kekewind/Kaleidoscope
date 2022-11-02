import time

import MyUtils

out = MyUtils.RefreshTXT('D:/url.txt')
month_dict = {}
day_dict = {}
for i in range(1, 12 + 1):
    month_dict.update({str(i).zfill(2): i})
month_to_day = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
for month in month_dict.keys():
    for day in range(month_to_day[month]):
        for h in ['pr', 'tas', 'tasmax', 'tasmin', 'rsds']:
            out.add('https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V2/GLOBAL/daily/' + h + '/CHELSA_' + h + '_' + str(day + 1).zfill(
                2) + '_' + month + '_1980_V.2.1.tif ')
out.save()

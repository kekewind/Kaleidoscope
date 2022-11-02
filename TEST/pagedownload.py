import MyUtils

url = 'https://gimg3.baidu.com/search/src=http%3A%2F%2Fpics1.baidu.com%2Ffeed%2Fa08b87d6277f9e2fcde08b9183bae72fba99f3ec.jpeg%3Ftoken%3Dbd7e500d5af4888f5fbd0540a8859526&refer=http%3A%2F%2Fwww.baidu.com&app=2021&size=f360,240&n=0&g=0n&q=75&fmt=auto?sec=1665075600&t=bf93462238e2fe36c538ad36aa3f3ac9'
path = MyUtils.desktoppath('1.png')
MyUtils.pagedownload(url, path, t=1)

import MyUtils

allpieces=MyUtils.RefreshJson('D:/Kaleidoscope/璐琪/AllPieces.txt')

def simplinfo(s):
    return s

def makerecord():
    for date in MyUtils.listdir('./璐琪/'):
        for p in MyUtils.listfile(date):
            s=simplinfo(MyUtils.filename(p))
            if not s in MyUtils.keys(allpieces.d):
                allpieces.add({s:[MyUtils.diskname]})
            else:
                allpieces.add({s:[allpieces.d[s],MyUtils.diskname]})

def  main():
    pass


if __name__=='__main__':
    main():

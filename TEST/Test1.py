import os


def CreatePath(path):
    """
    :param path: ’\‘自动转换为‘/’
    :return: 不返回值
    """
    if not path.rfind('.') > 1:
        path = path + '/'
    while path.rfind('//') > 0:
        path = re.sub('//', '/', path)
    if path.rfind('/') > 0:
        path = path[0:path.rfind('/')]
    else:
        path = path[0:path.rfind('\\')]
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print(f'Create {path} Failed. ')


def file(mode, path, IOList=None, encoding='utf-8'):
    CreatePath(path)
    # 比特流
    if mode == 'rb':
        with open(path, mode='rb') as file:
            if IOList == None:
                return (file.readlines())
            else:
                IOList = file.readlines()
                return
    # 字符流
    elif mode == 'r':
        if not IOList == None:
            with open(path, mode='r', encoding=encoding) as file:
                IOList = file.readlines()
                return
        if not os.path.exists(path):
            CreatePath('w', path, [])
            # warn(f'{path} get before this file exists.')
            return []
        with open(path, mode='r', encoding=encoding) as file:
            return (file.readlines())
    elif mode == 'rs':
        if not os.path.exists(path):
            file('w', path, [])
            return []
        with open(path, mode='r', encoding='utf-8') as file:
            content = file.readlines()
            newset = list(set(content))
            newset.sort(key=content.index)
            file('w', path, newset)
            if not IOList == []:
                IOList = newset
                return
            return newset
    elif mode == 'w':
        with open(path, mode='w', encoding=encoding) as file:
            file.writelines(IOList)
    elif mode == 'wb':
        try:
            with open(path, mode='wb') as file:
                file.write(IOList)
        except:
            with open(path, mode='wb') as file:
                file.writelines(IOList)


l1 = []
l2 = []
f1 = file('rb', 'D:/Kaleidoscope/TEST/Test1.mp4', l1)
f2 = file('wb', 'D:/Kaleidoscope/TEST/Test2.mp4', l1)

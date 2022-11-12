import os

import MyUtils

# https://www.jb51.net/article/224285.htm
with os.popen(f'cd d:;cd{MyUtils.projectpath()};', "r") as p:
    r = p.read()
print(r)


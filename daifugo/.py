from pathlib import Path as p
import sys
import os

imgpath = p.cwd()/'daifugo'/'assets'/'cards'

filelist = imgpath.glob("*.png")
print(filelist)
for file in filelist:
    if list(str(file))[0] in ['C', 'D', "H", "S"]:
        li = list(str(file))
        tmp = li[0]
        li[0]=li[1]
        li[1] = tmp
        li = ''.join(li)
        print(li)
    else : continue
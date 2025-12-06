import os
import pathlib
from pathlib import Path

_cd=""
def _display_directory(_list):
    for i in _list:
        print("├──"+i)
        _cd=_now_directory+"\\"+i
        if not Path(_cd).is_file():
            print("│    ├──",os.listdir(Path(_cd)))


_now_directory=input("現在の絶対パスを入力してください")

#C:\Users\skazu\Documents\python #test用
_directory_list=os.listdir(_now_directory)
#print(os.listdir(_now_directory))
f=Path(_now_directory)
print(f.is_file())

print(_now_directory)
_display_directory(_directory_list)

import os
import pathlib
from pathlib import Path


def _display_directory(_cd, _list,_level):
    for i in _list:
        target_path = _cd / i
        #if _list.index(i)==len(_list):
        #    print("│ "*_level+"└──"+i)
        print("│ "*_level+"├─"+i)
        if not Path(target_path).is_file():
            #print("│    ├──",os.listdir(Path(_cd)))
            _display_directory(target_path, os.listdir(target_path),_level+1)

_now_directory=input("現在の絶対パスを入力してください")

#C:\Users\skazu\Documents\python #test用
_directory_list=os.listdir(_now_directory)
_now_directory=Path(_now_directory)
print(_now_directory)
_cd=_now_directory
_display_directory(_now_directory,_directory_list,0)
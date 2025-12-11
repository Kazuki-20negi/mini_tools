import os
import pathlib
from pathlib import Path
RED = '\033[31m'
BLUE = '\033[34m'
GREEN = '\033[32m'
RESET = '\033[0m'

def _display_directory(_cd, _list,_prefix, a):
    for i in _list:
        target_path = _cd / i
        if i==a:
            pass
        elif _list.index(i)==len(_list)-1:
            if not Path(target_path).is_file():
                print(_prefix+"└─"+GREEN+i+RESET)
                _display_directory(target_path, os.listdir(target_path),_prefix+"  ",a)
            else:
                print(_prefix+"└─"+i)

        else:
            if not Path(target_path).is_file():
                print(_prefix+"├─"+GREEN+i+RESET)
                _display_directory(target_path, os.listdir(target_path),_prefix+"│ ",a)
            else:
                print(_prefix+"├─"+i)
        #if not Path(target_path).is_file():
        #    _display_directory(target_path, os.listdir(target_path),_prefix)


def setting():
    global a
    a=input("除外するパス:")


_now_directory=input("現在の絶対パスを入力してください")
if _now_directory=="setting":
    setting()
_now_directory=input("現在の絶対パスを入力してください")

#C:\Users\skazu\Documents\python #test用


_now_directory=Path(_now_directory)
_directory_list=os.listdir(_now_directory)
print(_now_directory)
_cd=_now_directory
_display_directory(_now_directory,_directory_list,"",a)
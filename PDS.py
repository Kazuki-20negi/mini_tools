import os
import pathlib
from pathlib import Path
RED = '\033[31m'
BLUE = '\033[34m'
GREEN = '\033[32m'
RESET = '\033[0m'
_except_list=[]

def _display_directory(_cd, _list,_prefix, _except_list):
    for index, i in enumerate(_list):
        target_path = _cd / i
        if not Path(target_path).is_file():
            i2=GREEN+i+RESET
        else:i2=i

        if index == len(_list) - 1:
            if not Path(target_path).is_file() and not i in _except_list:
                print(_prefix+"└─"+i2)
                _display_directory(target_path, os.listdir(target_path),_prefix+"  ",_except_list)
            else:
                print(_prefix+"└─"+i2)

        else:
            if not Path(target_path).is_file() and not i in _except_list:
                print(_prefix+"├─"+i2)
                _display_directory(target_path, os.listdir(target_path),_prefix+"│ ",_except_list)
            else:
                print(_prefix+"├─"+i2)
        #if not Path(target_path).is_file():
        #    _display_directory(target_path, os.listdir(target_path),_prefix)


def setting():
    global _except_list
    _except_list=input("中身を参照しないフォルダ名(,区切りスペースなし):").split(",")


_now_directory=input("絶対パスを入力,または'setting'で設定に移行")
if _now_directory=="setting":
    setting()
_now_directory=input("現在の絶対パスを入力してください")

#C:\Users\skazu\Documents\python #test用


_now_directory=Path(_now_directory)
_directory_list=os.listdir(_now_directory)
print(_now_directory)
_cd=_now_directory
_display_directory(_now_directory,_directory_list,"",_except_list)
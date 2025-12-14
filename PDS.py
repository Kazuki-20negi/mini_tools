import os
import pathlib
from pathlib import Path
import subprocess
RED = '\033[31m'
BLUE = '\033[34m'
GREEN = '\033[32m'
RESET = '\033[0m'
_except_list=[]
_output_lines=""

def _file_size(_path): #ファイルサイズを単位付きで返す
    _size=float(os.path.getsize(_path))
    if os.path.getsize(_path)>=1024:
        _size=_size/1024
        if _size>=1024:
            _size=_size/1024
            if _size>=1024:
                _size=_size/1024
                return " ("+f"{_size:.1f}GB)"
            return " ("+f"{_size:.1f}MB)"
        return " ("+f"{_size:.1f}KB)"
    else:
        return " ("+f"{_size:.1f}B)"

def _display_directory(_cd, _list,_prefix, _except_list):
    #ディレクトリツリーを表示
    global _output_lines
    for index, i in enumerate(_list):
        target_path = _cd / i
        if not Path(target_path).is_file():
            i2=GREEN+i+RESET#+_file_size(target_path)
        else:i2=i+_file_size(target_path)

        if index == len(_list) - 1:
            if not Path(target_path).is_file() and not i in _except_list:
                print(_prefix+"└─"+i2)
                _output_lines+=(_prefix+"└─"+i+"\n")
                _display_directory(target_path, sorted(os.listdir(target_path)),_prefix+"  ",_except_list)
            else:
                print(_prefix+"└─"+i2)
                _output_lines+=(_prefix+"└─"+i+"\n")

        else:
            if not Path(target_path).is_file() and not i in _except_list:
                print(_prefix+"├─"+i2)
                _output_lines+=(_prefix+"├─"+i+"\n")
                _display_directory(target_path, sorted(os.listdir(target_path)),_prefix+"│ ",_except_list)
            else:
                print(_prefix+"├─"+i2)
                _output_lines+=(_prefix+"├─"+i+"\n")

def setting(): #特定フォルダの除外
    global _except_list
    _except_list=input("中身を参照しないフォルダ名(,区切りスペースなし):").split(",")

def copy_clipboard(_output_lines): #クリップボードへのコピー
    subprocess.run("clip", input=_output_lines, text=True, encoding='cp932') 
    print("クリップボードにコピーしました！")


while True: # ユーザ入力の受付とエラーチェック
    _now_directory=input("絶対パスを入力,または'setting'で設定に移行")
    if _now_directory=="setting":
        setting()
        _now_directory=input("絶対パスを入力してください")

    else:
        if not Path(_now_directory).exists():
            print(f"{RED}エラー: 指定されたパスが見つかりません。もう一度入力してください。{RESET}")
            continue
        if not Path(_now_directory).is_dir():
            print(f"{RED}エラー: ファイルが指定されています。フォルダのパスを入力してください。{RESET}")
            continue

    try:
        _temp_list_a=sorted(os.listdir(_now_directory))
        break
    except PermissionError:
        print(f"{RED}エラー: アクセス権限がありません。別の場所を指定してください。{RESET}")
        continue
    except Exception as e:
        print(f"{RED}エラー: {e}{RESET}")
        continue

_output_lines+=(_now_directory+"\n")
_now_directory=Path(_now_directory)
_directory_list=sorted(os.listdir(_now_directory))
print(_now_directory)
_cd=_now_directory
_display_directory(_now_directory,_directory_list,"",_except_list)
if input("クリップードにコピーしますか？ (y/n):").lower()=="y":
    copy_clipboard(_output_lines)
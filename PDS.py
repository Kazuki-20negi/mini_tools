import os
import pathlib
from pathlib import Path
import subprocess
RED = '\033[31m'
BLUE = '\033[34m'
GREEN = '\033[32m'
RESET = '\033[0m'
except_list=[]
output_lines=""

def file_size(path): #ファイルサイズを単位付きで返す
    size=float(os.path.getsize(path))
    for unit in ["B","KB","MB","GB","TB"]:
        if size < 1024.0:
            return f"({size:.1f}{unit})"
        size /= 1024.0
    return f"({size:.1f}PB)"

def display_directory(current_dir, _list,prefix, except_list):
    #ディレクトリツリーを表示
    global output_lines
    for index, i in enumerate(_list):
        target_path = current_dir / i
        if not Path(target_path).is_file():
            i2=GREEN+i+RESET#+file_size(target_path)
        else:i2=i+file_size(target_path)

        if index == len(_list) - 1:
            if not Path(target_path).is_file() and not i in except_list:
                print(prefix+"└─"+i2)
                output_lines+=(prefix+"└─"+i+"\n")
                display_directory(target_path, sorted(os.listdir(target_path)),prefix+"  ",except_list)
            else:
                print(prefix+"└─"+i2)
                output_lines+=(prefix+"└─"+i+"\n")

        else:
            if not Path(target_path).is_file() and not i in except_list:
                print(prefix+"├─"+i2)
                output_lines+=(prefix+"├─"+i+"\n")
                display_directory(target_path, sorted(os.listdir(target_path)),prefix+"│ ",except_list)
            else:
                print(prefix+"├─"+i2)
                output_lines+=(prefix+"├─"+i+"\n")

def setting(): #特定フォルダの除外
    global except_list
    except_list=input("中身を参照しないフォルダ名(,区切りスペースなし):").split(",")

def copy_clipboard(output_lines): #クリップボードへのコピー
    subprocess.run("clip", input=output_lines, text=True, encoding='cp932') 
    print("クリップボードにコピーしました！")


while True: # ユーザ入力の受付とエラーチェック
    now_directory=input("絶対パスを入力,または'setting'で設定に移行")
    if now_directory=="setting":
        setting()
        now_directory=input("絶対パスを入力してください")

    else:
        if not Path(now_directory).exists():
            print(f"{RED}エラー: 指定されたパスが見つかりません。もう一度入力してください。{RESET}")
            continue
        if not Path(now_directory).is_dir():
            print(f"{RED}エラー: ファイルが指定されています。フォルダのパスを入力してください。{RESET}")
            continue

    try:
        directory_list=sorted(os.listdir(now_directory))
        break
    except PermissionError:
        print(f"{RED}エラー: アクセス権限がありません。別の場所を指定してください。{RESET}")
        continue
    except Exception as e:
        print(f"{RED}エラー: {e}{RESET}")
        continue

output_lines+=(now_directory+"\n")
now_directory=Path(now_directory)
print(now_directory)
current_dir=now_directory
display_directory(now_directory,directory_list,"",except_list)
if input("クリップードにコピーしますか？ (y/n):").lower()=="y":
    copy_clipboard(output_lines)
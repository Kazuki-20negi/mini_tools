import os
import pathlib

_now_directory=input("現在の絶対パスを入力してください")

print(os.listdir(_now_directory))
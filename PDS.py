import os
import pathlib

_now_directory=input("現在の絶対パスを入力してください")
#C:\Users\skazu\Documents\python #test用
_directory_list=os.listdir(_now_directory)
#print(os.listdir(_now_directory))

print(_now_directory)
for i in _directory_list:
    print("├──"+i)
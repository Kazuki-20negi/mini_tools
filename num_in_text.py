import re
import sys

while True:
    print("入力してください：")
    text=sys.stdin.read()
    num=re.findall(r"\d+",text)
    total=sum(int(n) for n in num)
    print(f"合計：{total}")
    print("-"*20)

import re
from collections import defaultdict

def search_in_file(file_path, pattern):
    data=[]
    match_count=0
    with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if re.search(r"^\d{4}/\d{2}/\d{2}",line):
                     data.append(line.strip())
                if re.search(pattern, line):
                    #print(f"{i}行目: {data[-1]}{line.strip()}")
                    match_count+=1
    return match_count


def count_user_speaking(file_path, pattern):
    char_counts = defaultdict(int)
    speak_pattern=re.compile(r"^(\d{2}:\d{2})\t([^\t]+)\t(.*)$")
    user_regex=re.compile(pattern)
    current_user=None
    with open(file_path, "r", encoding="utf-8") as f:
         for line in f:
                line = line.rstrip('\n') # 行末の改行のみ削除
                match = speak_pattern.match(line)
                
                if match:
                    time_str, user_name, message = match.groups()
                    
                    # ユーザー名が指定条件にマッチするか
                    if user_regex.search(user_name):
                        current_user = user_name
                        # LINEの仕様で改行を含むメッセージは前後に"が付くことがあるため除去
                        clean_msg = message.strip('"')
                        char_counts[current_user] += len(clean_msg)
                    else:
                        current_user = None # 対象外のユーザー
                else:
                    # 継続行（前の行の続き）の場合
                    if current_user:
                        clean_msg = line.strip('"')
                        char_counts[current_user] += len(clean_msg)
                        
    return char_counts
file_name="hogehoge.txt"

#print("---参加ログ---")
#search_in_file(file_name, r"が参加しました")
#print("\n---退会ログ---")
#search_in_file(file_name, r"が退会しました")
print(f"累計参加者：{search_in_file(file_name, r"が参加しました")}人")

print("\n---発言字数---")
print(dict(count_user_speaking(file_name,r"20本ネギ")))
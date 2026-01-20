import re

def search_in_file(file_path, pattern):
    data=[]
    with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if re.search(r"^\d{4}/\d{2}/\d{2}",line):
                     data.append(line.strip())
                if re.search(pattern, line):
                    print(f"{i}行目: {data[-1]}{line.strip()}")
file_name="test.txt"

print("---参加ログ---")
search_in_file(file_name, r"が参加しました")
print("--------------\n---退会ログ---")
search_in_file(file_name, r"が退会しました")
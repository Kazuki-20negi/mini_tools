import re

def search_in_file(file_path, pattern):
    with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if re.search(pattern, line):
                    print(f"{i}行目: {line.strip()}")
search_in_file("test.txt", r"が参加しました")
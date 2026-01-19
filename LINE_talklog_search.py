import re

def search_in_file(file_path, pattern):
    with open(file_path, "r", encoding="utf-8") as f:
        content= f.read()
    matches= re.findall(pattern, content, re.MULTILINE)
    for match in matches:
        print(f"Found: '{match.group()}' at position {match.start()}-{match.end()}")

search_in_file("test.txt", r"が参加しました")
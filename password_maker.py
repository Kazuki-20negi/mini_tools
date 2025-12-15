import secrets
import argparse
import string

def get_unicode_range(start, end):
    """指定した範囲のユニコード文字を文字列として返す関数"""
    return "".join(chr(c) for c in range(start, end))

#パーサ作成
parser = argparse.ArgumentParser(description='password maker')
parser.add_argument("length",help="パスワードの桁数")
parser.add_argument("-u", "--unicode", action="store_true", help="ユニコード文字（ひらがな・漢字など）を含める")

args = parser.parse_args()

#文字種定義
alphabet = string.ascii_letters + string.digits
punctuation = "-*/._:;[]#()"
candidates = alphabet + punctuation

if args.unicode: #ひらがなと漢字一部
    hiragana = get_unicode_range(0x3041, 0x3097)
    kanji = get_unicode_range(0x4E00, 0x4E50)
    candidates += hiragana+kanji

#パスワード生成
while True:
    password="".join(secrets.choice(candidates)for i in range(int(args.length)))
    if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password)>=2
            and any(c in punctuation for c in password)):
        break

print(password)
import secrets
import argparse
import string

#パーサ作成
parser = argparse.ArgumentParser(description='password maker')
parser.add_argument("arg1",help="桁数")
args = parser.parse_args()

#文字種定義
alphabet = string.ascii_letters + string.digits
punctuation = "-*/._:;[]#()"

#パスワード生成
while True:
    password="".join(secrets.choice(alphabet+punctuation)for i in range(int(args.arg1)))
    if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password)>=2
            and any(c in punctuation for c in password)):
        break

print(password)
import secrets
import argparse
import string
parser = argparse.ArgumentParser(description='password maker')    # 2. パーサを作る
parser.add_argument("arg1",help="桁数")
args = parser.parse_args()

#a=secrets.token_urlsafe(int(args.arg1))
#print(a[0:int(args.arg1)])
alphabet = string.ascii_letters + string.digits
punctuation = "-*/._:;[]#()"
while True:
    password="".join(secrets.choice(alphabet+punctuation)for i in range(int(args.arg1)))
    if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password)>=2
            and any(not(c.isalnum()) for c in password)):
        break
print(password)
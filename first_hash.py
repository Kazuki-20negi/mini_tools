import hashlib

text="はじめてのハッシュ"
byte_text=text.encode("utf-8")

hash_object=hashlib.sha512(byte_text)
hex_dig=hash_object.hexdigest()

print(hex_dig)
print(f"len:{len(hex_dig)}")
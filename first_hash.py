import hashlib

text="はじめてのハッシュ"
byte_text=text.encode("utf-8")

hash_object=hashlib.sha512(byte_text)
hex_dig=hash_object.hexdigest()

print(hex_dig)
print(f"len:{len(hex_dig)}")

# 同一文字列からは同一のハッシュ
hash_object2=hashlib.sha512(byte_text)
hex_dig2=hash_object2.hexdigest()

print("\n同一文字列をハッシュ化")
print(hex_dig2)
print(f"len:{len(hex_dig2)}")

import hashlib

text="はじめてのハッシュ"
byte_text=text.encode("utf-8")

hash_object=hashlib.sha256(byte_text)
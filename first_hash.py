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

# ハッシュによる改ざん判定
text_base="改ざん検知のテスト1"
text_same="改ざん検知のテスト1"
text_diff="改ざん検知のテスト2"

def calculate_hash(text):
    """文字列を受け取り、SHA-256ハッシュ値を返す関数"""
    # バイト列に変換
    byte_data = text.encode('utf-8')
    # ハッシュ化
    hex_digest = hashlib.sha256(byte_data).hexdigest()
    return hex_digest
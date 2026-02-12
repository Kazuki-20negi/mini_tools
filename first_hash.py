import hashlib

text="はじめてのハッシュ"
byte_text=text.encode("utf-8")

hash_object=hashlib.sha512(byte_text)
hex_dig=hash_object.hexdigest()

print(f"はじめてのハッシュ：{hex_dig}")
print(f"len:{len(hex_dig)}")

# 同一文字列からは同一のハッシュ
hash_object2=hashlib.sha512(byte_text)
hex_dig2=hash_object2.hexdigest()

print("\n同一文字列をハッシュ化")
print(hex_dig2)
print(f"len:{len(hex_dig2)}")

# ハッシュによる改ざん判定
print("-" * 60)
def calculate_hash(text):
    """文字列を受け取り、SHA-256ハッシュ値を返す関数"""
    # バイト列に変換
    byte_data = text.encode('utf-8')
    # ハッシュ化
    hex_digest = hashlib.sha256(byte_data).hexdigest()
    return hex_digest

text_base="改ざん検知のテスト1"
text_same="改ざん検知のテスト1"
text_diff="改ざん検知のテスト2"

hash_base = calculate_hash(text_base)
hash_same = calculate_hash(text_same)
hash_diff = calculate_hash(text_diff)

print(f"Hash(基準): {hash_base[:10]}...")
print(f"Hash(同じ): {hash_same[:10]}...")
print(f"Hash(違う): {hash_diff[:10]}...")

print(f"基準＝＝同じ：{hash_base==hash_same}")
print(f"基準＝＝違う：{hash_base==hash_diff}")

# 簡易版ハッシュアルゴリズム
def my_hash(raw_text):
    h1=11
    h2=23
    h3=27
    h4=3
    block_size=4
    raw_text+="0"*(len(raw_text)%4) #パディング
    for i in range(0, len(raw_text), block_size):
        temp=h1+raw_text[i:i+block_size]
        

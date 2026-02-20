
key="abc"
text="helloworld"

def stream_encrypt(text,key):
    key=key*(len(text)//len(key))+key[:len(text)%len(key)]
    result=""
    for i in range(len(text)):
        xor_val=ord(text[i])^ord(key[i])
        result+=f"{xor_val:02x}"
        #result+=chr(xor_val)
    return result

encrypted_text = stream_encrypt(text, key)
print(encrypted_text)

def stream_decrypt(hex_cipher,key):
    pass